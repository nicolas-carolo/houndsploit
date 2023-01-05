from flask import request
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode


def get_exploit_from_params(request):
    exploit_id = request.args.get('exploit-id', None)
    exploit = Exploit.get_by_id(exploit_id)
    return exploit


def get_shellcode_from_params(request):
    shellcode_id = request.args.get('shellcode-id', None)
    shellcode = Shellcode.get_by_id(shellcode_id)
    return shellcode

