import json
import os
import subprocess
import sys
FORMAT = 1


def __main__(argv: list[str] = None):
  if argv is None:
    argv = sys.argv
  if len(argv) != 2:
    raise Exception("Incorrect launch arguments")
  with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)["MainServiceAPI/wrapper"]
  if data["format"] != FORMAT:
    raise Exception("Incorrect data format")
  if "platforms" in data:
    if type(data["platforms"]) == str:
      data["platforms"] = [data["platforms"]]
      print("Warning: the parameter 'platforms' should be a list, not a string", file=sys.stderr)
    if not sys.platform in data["platforms"]:
      raise Exception("Supported platforms: %s" % ", ".join(data["platforms"]))
  kw = {}
  kw["args"] = data["args"]
  if "cwd" in data:
    kw["cwd"] = data["cwd"]
  if "env" in data:
    kw["env"] = {}
    if not data.get("clear_env"):
      for k, v in os.environ.items():
        kw["env"][k] = v
    for k, v in data["env"].items():
      kw["env"][k] = str(v)
  if "exe" in data:
    kw["executable"] = data["exe"]
  for i in ["stderr", "stdin", "stdout"]:
    if i in data:
      kw[i] = open(data[i], ("rb" if i == "stdin" else "wb"))
  code = subprocess.call(**kw)
  for i in ["stderr", "stdin", "stdout"]:
    if i in kw:
      kw[i].close()
  return code


if __name__ == "__main__":
  exit(__main__())
