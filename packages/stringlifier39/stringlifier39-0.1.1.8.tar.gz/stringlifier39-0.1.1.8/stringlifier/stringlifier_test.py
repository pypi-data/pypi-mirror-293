from stringlifier.api import Stringlifier

stringlifier=Stringlifier()

s = stringlifier("com.docker.hyperkit -A -u -F vms/0/hyperkit.pid -c 8 -m 8192M -b 127.0.0.1 --pass=\"NlcXVpYWRvcg\" -s 0:0,hostbridge -s 31,lpc -s 1:0,virtio-vpnkit,path=vpnkit.eth.sock,uuid=45172425-08d1-41ec-9d13-437481803412 -U c6fb5010-a83e-4f74-9a5a-50d9086b9")

print(s)