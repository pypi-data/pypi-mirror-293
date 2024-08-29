local ip="192.168.2.12"
local port=4001
local err=0
local socket=0
local Option="CP=1 Speed=100 Accel=20 SYNC=1"
function yd(dian,f)
  Go(P0,Option)
  Go(RP(dian,{0,0,90}),Option)
  Go(dian,Option)
  DO(1,f)
  Go(RP(dian,{0,0,90}),Option)
  Go(P0,Option)
end
Go(P0,Option)
while true do
	::create_server::
	err, socket = TCPCreate(false, ip, port)
	if err ~= 0 then
		print("无法创建socket,正在重新连接")
		Sleep(1000)
		goto create_server
	end
	err = TCPStart(socket, 0)
	if err ~= 0 then
		print("无法连接服务器,正在重新连接")
		TCPDestroy(socket)
		Sleep(1000)
		goto create_server
	end
	while true do
		err, buf = TCPRead(socket, 0,"string")
		data =buf.buf
		if err ~= 0 then
			print("读取数据失败,正在重新连接")
			TCPDestroy(socket)
			Sleep(1000)
			break
		end
		print("接收数据:",data)
    local data1=string.sub(data,0,4)
    local data2=string.sub(data,5,6)
    print("接收数据:",data1)
    print("接收数据:",data2)
    if data1 =="qewm" or data1=="qzf_" or data1=="qry_"then
      if data2 =="01" then
        yd(P1,1)
      elseif data2=="02" then
        yd(P2,1)
      elseif data2=="03" then
        yd(P3,1)
      elseif data2=="04" then
        yd(P4,1)
      elseif data2=="05" then
        yd(P5,1)
      elseif data2=="06" then
        yd(P6,1)
      elseif data2=="07" then
        yd(P7,1)
      elseif data2=="08" then
        yd(P8,1)
      elseif data2=="09" then
        yd(P9,1)
      elseif data2=="10" then
        yd(P10,1)
      elseif data2=="11" then
        yd(P11,1)
      elseif data2=="12" then
        yd(P12,1)
      end
      Go(P0,Option)
      yd(P14,0)
      Go(P0,Option)
      if data1 =="qewm" then
        TCPWrite(socket,"jqr_plc_pai_ewm")
      elseif data1 =="qzf_" then
        TCPWrite(socket,"jqr_plc_pai_zf")
      elseif data1 =="qry_" then
        TCPWrite(socket,"jqr_plc_pai_ry")
    end
    if data1=="qkb_"then
      Go(P0,Option)
      yd(P1,1)
      Go(P0,Option)
      yd(P19,0)
      Go(P0,Option)
      TCPWrite(socket,"jqr_plc_pai_ys")
      yd(P19,1)
      Go(P0,Option)
      yd(P13,0)
      Go(P0,Option)
      TCPWrite(socket,"jqr_plc_ok")
    end
    if data1=="fewm" or data1=="fry_" or data1=="fwz_" or data1=="fsz_"then
      Go(P0,Option)
      yd(P14,1)
      Go(P0,Option)
      if data2=="01" then
        yd(P15,0)
      elseif data2=="02" then
        yd(P16,0)
      elseif data2=="03" then
        yd(P17,0)
      elseif data2=="04" then
        yd(P18,0)
      end
    Go(P0,Option)
      if data1=="fewm" then
        TCPWrite(socket,"jqr_plc_ewm_again")
      elseif data1=="fry_" then
        TCPWrite(socket,"jqr_plc_ry_again")
      elseif data1=="fwz_" then
        TCPWrite(socket,"jqr_plc_fafang_again")
    end
  end
end