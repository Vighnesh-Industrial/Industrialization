#!/usr/bin/env python3
"""Produce the hosted build of the workbench from index.html.

index.html is the source of truth; it is a complete standalone document meant
to be opened from disk. The hosted page differs in exactly three ways, applied
here rather than kept as a second copy that drifts:

  1. The publish skeleton supplies <!doctype>, <head> and <body>, so the
     document wrapper is removed and the file starts at its own <title>.
  2. The sticky top bar clears the phone's status bar.
  3. Saving a file works differently in the hosted sandbox, which blocks
     downloads a page starts itself.

Run:  python3 build-artifact.py
"""
import re, sys, pathlib

SRC = pathlib.Path("index.html")
OUT = pathlib.Path("dist/workbench.html")
s = SRC.read_text()

# 1. strip the document wrapper - keep everything from <title> to </script>
start = s.index("<title>")
end = s.rindex("</script>") + len("</script>")
s = s[start:end]
for tag in ("</head>", "<body>", "</style>\n</head>\n<body>"):
    pass
s = s.replace("</head>\n<body>\n", "", 1)
assert "<body>" not in s and "</head>" not in s, "document wrapper not fully removed"

# 2. sticky header clears the safe-area inset
old = ".topbar{position:sticky;top:0;"
new = ".topbar{position:sticky;top:env(safe-area-inset-top, 0px);"
assert old in s
s = s.replace(old, new, 1)

# 3. saving a file
old_dl = '''function download(name, text, mime){
  const blob = new Blob([text],{type:(mime||"application/json")+";charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href=url; a.download=name; document.body.appendChild(a); a.click();
  setTimeout(()=>{URL.revokeObjectURL(url); a.remove();},0);
}'''
new_dl = '''/* Two places this page runs, and they save files differently.

   Opened from disk it is an ordinary browser download. Served as a hosted
   page the sandbox blocks a download the page starts itself, so the viewer's
   shell is asked to save instead — it shows a confirmation and the viewer may
   decline. If neither route is open the text goes to the clipboard, because
   losing an export you asked for is worse than an extra paste. */
let _saver, _saverAsked = false;
async function download(name, text, mime){
  if(!_saverAsked){
    _saverAsked = true;
    try{ _saver = (window.claude && window.claude.use) ? await window.claude.use("downloads") : null; }
    catch(e){ _saver = null; }
  }
  if(_saver){
    try{
      await _saver.save({filename:name, data:text});
      toast("Saved " + name);
      return;
    }catch(err){
      const code = err && err.code;
      if(code === "declined") return;               // the viewer said no; that is an answer
      if(code === "rate_limited"){ toast("A save is already open — finish that one first"); return; }
      // anything else: fall through to the routes below
    }
  }
  try{
    const blob = new Blob([text],{type:(mime||"application/json")+";charset=utf-8"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href=url; a.download=name; document.body.appendChild(a); a.click();
    setTimeout(()=>{URL.revokeObjectURL(url); a.remove();},0);
    return;
  }catch(e){ /* blocked — clipboard below */ }
  try{
    await navigator.clipboard.writeText(text);
    toast(name + " copied to the clipboard — paste it into a file");
  }catch(e){
    alert("This page cannot save files here. Copy the text below into " + name + ":\\n\\n" + text.slice(0, 2000) +
          (text.length > 2000 ? "\\n\\n… truncated. Open the tool from a local copy to export in full." : ""));
  }
}'''
assert old_dl in s, "download() not found — has index.html changed?"
s = s.replace(old_dl, new_dl, 1)

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(s)
print(f"{OUT}  {len(s):,} bytes")
print("starts:", s[:60].replace("\n", " "))
print("ends  :", s[-40:].replace("\n", " "))
