IF "shou1".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "a语音".r_data[#i] = ',' OR "a语音".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "a语音".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "a语音".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    "a语音".r_data := "a语音".e_data;
    IF "a语音".u_data[0] = 'yy_plc_ewm' THEN
        "发送"(buf := 'qewm08',
             num := 4);
    END_IF;
    IF "a语音".u_data[0] = 'yy_plc_zf' THEN
        "发送"(buf := 'qzf_02',
             num := 4);
    END_IF;
    IF "a语音".u_data[0] = 'yy_plc_kb' THEN
        "发送"(buf := 'qkb_01',
             num := 4);
    END_IF;
    IF "a语音".u_data[0] = 'yy_plc_ry' THEN
        "发送"(buf := 'qry_03',
             num := 4);
    END_IF;
END_IF;
////////////////////////////////////////////////////////////////////////////////////////////////////
IF "shou2".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "b图像".r_data[#i] = ',' OR "b图像".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "b图像".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "b图像".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    "b图像".r_data := "b图像".e_data;
    FOR #i:= 0 TO 7 DO
        IF "b图像".u_data[0] = "b图像".wz[#i] THEN
            "b图像".biao[#i] := 1;
        ELSE
            "发送"(buf := 'yiqi',
                 num := 4);
        END_IF;
    END_FOR;
    IF "b图像".u_data[0] = 'tx_plc_wzsb' THEN
        FOR #i := 2 TO 3 DO
            IF "b图像".u_data[1] = "c视觉".r1[#i] AND("b图像".biao[0]=0 OR "b图像".biao[1]=0)  THEN
                "发送"(buf := 'fwz_01',
                     num := 4);
            ELSIF "b图像".u_data[1] = "c视觉".r2[#i]  AND("b图像".biao[2]=0 OR "b图像".biao[3]=0) THEN
                "发送"(buf := 'fwz_02',
                     num := 4);
            ELSIF "b图像".u_data[1] = "c视觉".r3[#i]  AND("b图像".biao[4]=0 OR "b图像".biao[5]=0) THEN
                "发送"(buf := 'fwz_03',
                     num := 4);
            ELSIF "b图像".u_data[1] = "c视觉".r4[#i]  AND("b图像".biao[6]=0 OR "b图像".biao[7]=0) THEN
                "发送"(buf := 'fwz_04',
                     num := 4);
            END_IF;
        END_FOR;
    END_IF;
END_IF;
//////////////////////////////////////////////////////////////////////////////////////////
IF "shou3".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "c视觉".r_data[#i] = ',' OR "c视觉".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "c视觉".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "c视觉".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    "c视觉".r_data := "c视觉".e_data;
    IF "c视觉".u_data[0] = 'sj_plc_ewm' THEN
        IF "c视觉".u_data[1] = 'low' THEN
            "发送"(buf := 'fewm01',
                 num := 4);
            "ff触摸屏信号".界面1[1] := 1;
        END_IF;
        IF "c视觉".u_data[1] = 'mid' THEN
            "发送"(buf := 'fewm02',
                 num := 4);
            "ff触摸屏信号".界面1[2] := 1;
        END_IF;
        IF "c视觉".u_data[1] = 'high' THEN
            "发送"(buf := 'fewm03',
                 num := 4);
            "ff触摸屏信号".界面1[3] := 1;
        END_IF;
    ELSIF "c视觉".u_data[0] = 'sj_plc_zf' THEN
        IF "c视觉".u_data[1] = '1' THEN
            "发送"(buf := 'fsz_04',
                 num := 4);
            "ff触摸屏信号".界面1[4] := 1;
        END_IF;
        IF "c视觉".u_data[1] = '2' THEN
            "发送"(buf := 'fsz_04',
                 num := 4);
            "ff触摸屏信号".界面1[5] := 1;
        END_IF;
        IF "c视觉".u_data[1] = '3' THEN
            "发送"(buf := 'fsz_04',
                 num := 4);
            "ff触摸屏信号".界面1[6] := 1;
        END_IF;
    ELSIF "c视觉".u_data[0] = 'sj_plc_pai_ok' THEN
        "发送"(buf := 'plc_tx_wzsb',
             num := 2);
    ELSIF "c视觉".u_data[0] = 'sj_plc_ry' THEN
        IF "c视觉".u_data[2] = '2018' THEN
            "发送"(buf := 'fry_01',
                 num := 4);
            "c视觉".u_data[2] := '16';

        ELSIF "c视觉".u_data[2] = '2008' THEN
            "发送"(buf := 'fry_02',
                 num := 4);
            "c视觉".u_data[2] := '26';
        ELSIF "c视觉".u_data[2] = '1998' THEN
            "发送"(buf := 'fry_03',
                 num := 4);
            "c视觉".u_data[2] := '36';
        ELSIF "c视觉".u_data[2] = '1988' THEN
            "发送"(buf := 'fry_04',
                 num := 4);
            "c视觉".u_data[2] := '46';
        END_IF;
        IF "renyuan_jishu" = 0 THEN
            FOR #i := 0 TO 3 DO
                "c视觉".r1[#i] := "c视觉".u_data[#i + 1];
            END_FOR;
            FOR #i := 2 TO 3 DO
                "b图像".wz[#i-2] := "c视觉".r1[#i];
            END_FOR;
        ELSIF "renyuan_jishu" = 1 THEN
            FOR #i := 0 TO 3 DO
                "c视觉".r2[#i] := "c视觉".u_data[#i + 1];
            END_FOR;
            FOR #i := 2 TO 3 DO
                "b图像".wz[#i] := "c视觉".r2[#i];
            END_FOR;
        ELSIF "renyuan_jishu" = 2 THEN
            FOR #i := 0 TO 3 DO
                "c视觉".r3[#i] := "c视觉".u_data[#i + 1];
            END_FOR;
            FOR #i := 2 TO 3 DO
                "b图像".wz[#i+2] := "c视觉".r3[#i];
            END_FOR;
        ELSIF "renyuan_jishu" = 3 THEN
            FOR #i := 0 TO 3 DO
                "c视觉".r4[#i] := "c视觉".u_data[#i + 1];
            END_FOR;
            FOR #i := 2 TO 3 DO
                "b图像".wz[#i+4] := "c视觉".r4[#i];
            END_FOR;
        END_IF;
    END_IF;
END_IF;
//////////////////////////////////////////////////////////////////////////
IF "shou4".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "d机器人".r_data[#i] = ',' OR "d机器人".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "d机器人".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "d机器人".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    "d机器人".r_data := "d机器人".e_data;
    IF "d机器人".u_data[0] = 'jqr_plc_pai_ewm' THEN
        "发送"(buf := 'plc_sj_pai_ewm',
             num := 3);
    ELSIF "d机器人".u_data[0] = 'jqr_plc_ewm_again' THEN
        "ewm_jishu" += 1;
        IF "ewm_jishu" < 3 THEN
            IF "ewm_jishu" = 1 THEN
                "发送"(buf := 'qewm10',
                     num := 4);
            END_IF;
            IF "ewm_jishu" = 2 THEN
                "发送"(buf := 'qewm12',
                     num := 4);
            END_IF;
        ELSE
            "发送"(buf := 'plc_yy_ok',
                 num := 1);
        END_IF;
    ELSIF "d机器人".u_data[0] = 'jqr_plc_pai_zf' THEN
        "发送"(buf := 'plc_sj_pai_zf',
             num := 3);
    ELSIF "d机器人".u_data[0] = 'jqr_plc_pai_ry' THEN
        "发送"(buf := 'plc_sj_pai_ry',
             num := 3);
    ELSIF "d机器人".u_data[0] = 'jqr_plc_ry_again' THEN
        "renyuan_jishu" += 1;
            IF "renyuan_jishu" < 4 THEN
                IF "renyuan_jishu" = 1 THEN
                    "发送"(buf := 'qry_04',
                         num := 4);
                END_IF;
                IF "renyuan_jishu" = 2 THEN
                    "发送"(buf := 'qry_05',
                         num := 4);
                END_IF;
                IF "renyuan_jishu" = 3 THEN
                    "发送"(buf := 'qry_06',
                         num := 4);
                END_IF;
            ELSE
                "发送"(buf := 'plc_yy_ok',
                     num := 1);
            END_IF;
        ELSIF "d机器人".u_data[0] = 'jqr_plc_fafang_again' THEN
            "发放信号" := 1;
        ELSIF "d机器人".u_data[0] = 'jqr_plc_ok' THEN
            "发送"(buf := 'plc_yy_ok',
                 num := 1);
        END_IF;
END_IF;
///////////////////////////////////////////////////////////////////////////////
F "shou5".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "e按钮".r_data[#i] = ',' OR "e按钮".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "e按钮".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "e按钮".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    "e按钮".r_data := "e按钮".e_data;
    IF "e按钮".u_data[0] = 'an_plc_fafang' THEN
        "发放信号" := 1;
    END_IF;
END_IF;
/////////////////////////////////////////////////////////////////////////////////
"发送长度" := LEN(#buf);
IF #num = 1 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "a语音".s_data);
    "发送标志" := 1;
END_IF;
IF #num = 2 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "b图像".s_data);
    "发送标志" := 1;
END_IF;
IF #num = 3 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "c视觉".s_data);
    "发送标志" := 1;
END_IF;
IF #num = 4 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "d机器人".s_data);
    "发送标志" := 1;
END_IF;
////////////////////////////////////////////////////////////////////////////////////
IF "发放信号" = 1 AND "物资检测" = 1 AND "到位检测" = 0 THEN
    "发放信号" := 0;
    "发放" := 1;
END_IF;

IF "d机器人".u_data[0] = 'jqr_plc_pai_ys' THEN
    "d机器人".u_data[0] := '0';
END_IF;
///////////////////////////////////////////////////////////////////////

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