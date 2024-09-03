import argparse
from MainServiceAPI.linux import make_wrapper
argp_kw = {}
argp_kw["epilog"] = "от MainPlay TG | https://t.me/MainPlay_TG"
# argp_kw["formatter_class"]=argparse.RawTextHelpFormatter


def make_svc():
  argp_kw["description"] = "Быстрое создание сервиса"
  argp_kw["prog"] = "MainServiceAPI-make_svc"
  argp = argparse.ArgumentParser(**argp_kw)
  argp.add_argument("-n", "--name", required=True, help="название сервиса (обязательно)")
  argp.add_argument("--autorestart", action="store_true", help="автоматический перезапуск сервиса при его завершении")
  argp.add_argument("--cwd", help="путь к рабочей папке")
  argp.add_argument("--description", help="описание сервиса")
  argp.add_argument("--exe", help="путь к исполняемому файлу")
  argp.add_argument("--on-boot", action="store_true", help="запуск при включении устройства")
  argp.add_argument("--restart-sec", type=float, help="задержка перезапуска в секундах")
  argp.add_argument("--stderr", help="путь к файлу stderr")
  argp.add_argument("--stdin", help="путь к файлу stdin")
  argp.add_argument("--stdout", help="путь к файлу stdout")
  argp.add_argument("--user", help="имя пользователя, от имени которого будет запущен сервис")
  argp.add_argument("args", nargs="+", help="аргументы для запуска сервиса")
  args = argp.parse_args()
  kw = {}
  kw["always_restart"] = bool(args.autorestart)
  kw["args"] = args.args
  kw["cwd"] = args.cwd
  kw["description"] = args.description
  kw["exe"] = args.exe
  kw["name"] = args.name
  kw["on_boot"] = bool(args.on_boot)
  kw["reload"] = True
  kw["restart_sec"] = float(args.restart_sec)
  kw["stderr"] = args.stderr
  kw["stdin"] = args.stdin
  kw["stdout"] = args.stdout
  kw["user"] = args.user
  svc_name = make_wrapper(**kw)
  print("Создан сервис под названием %r" % svc_name)
  return 0
