IF "shou1".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "aa语音".r_data[#i] = ',' OR "aa语音".r_data[#i] =0 THEN
            Chars_TO_Strg(Chars:="aa语音".r_data,
                          pChars:=#i_1,
                          Cnt:=#i-#i_1,
                          Strg=>"aa语音".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
            
        END_IF;
    END_FOR;
    "aa语音".r_data := "aa语音".e_data;
    IF "aa语音".u_data[0]='yy_plc_ewm' THEN
        "发送"(buf := 'qewm08',
             num := 4);
    ELSIF "aa语音".u_data[0]='yy_plc_sz' THEN
        "发送"(buf := 'qsz_02',
             num := 4);
    ELSIF "aa语音".u_data[0]='yy_plc_kb' THEN
        "发送"(buf := 'qkb_01',
             num := 4);
    ELSIF "aa语音".u_data[0]='yy_plc_ry' THEN
        "发送"(buf := 'qry_03',
             num := 4);

    END_IF;
END_IF;
———————————————————————
IF "shou2".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "bb图像".r_data[#i] = ',' OR "bb图像".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "bb图像".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "bb图像".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    "bb图像".r_data := "bb图像".e_data;
    IF "bb图像".u_data[0] = 'tx_plc_wz' THEN
        FOR #i := 2 TO 3 DO
            IF "bb图像".u_data[1] = "cc视觉".r1[#i] THEN
                "发送"(buf := 'fwz_15',
                     num := 4);
            ELSIF "bb图像".u_data[1] = "cc视觉".r2[#i] THEN
                "发送"(buf := 'fwz_16',
                     num := 4);
            ELSIF "bb图像".u_data[1] = "cc视觉".r3[#i] THEN
                "发送"(buf := 'fwz_17',
                     num := 4);
            ELSIF "bb图像".u_data[1] = "cc视觉".r4[#i] THEN
                "发送"(buf := 'fwz_18',
                     num := 4);
            END_IF;
        END_FOR;
        FOR #i := 0 TO 7 DO
            IF "bb图像".u_data[1] = "cc视觉".wzzl[#i] THEN
                "cc视觉".hmi[31 + #i] := 1;
            ELSE
                "发送"(buf := 'fwz_23',
                     num := 4);
            END_IF;
        END_FOR;
    END_IF;
END_IF;
————————————————————
IF "shou3".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "cc视觉".r_data[#i] = ',' OR "cc视觉".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "cc视觉".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "cc视觉".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
            
        END_IF;
    END_FOR;
    "cc视觉".r_data := "cc视觉".e_data;
    IF "cc视觉".u_data[0] = 'sj_plc_ewm' THEN
        IF "cc视觉".u_data[1] = 'low' THEN
            "发送"(buf := 'fewm15',
                 num := 4);
            "cc视觉".hmi[1] := 1;
        ELSIF "cc视觉".u_data[1] = 'mid' THEN
            "发送"(buf := 'fewm16',
                 num := 4);
            "cc视觉".hmi[2] := 1;
        ELSIF "cc视觉".u_data[1] = 'high' THEN
            "发送"(buf := 'fewm17',
                 num := 4);
            "cc视觉".hmi[3] := 1;
        END_IF;
    ELSIF "cc视觉".u_data[0] = 'sj_plc_sz' THEN
        IF "cc视觉".u_data[1] = '1' THEN
            "发送"(buf := 'fsz_18',
                 num := 4);
            "cc视觉".hmi[11] := 1;
        ELSIF "cc视觉".u_data[1] = '2' THEN
            "发送"(buf := 'fsz_18',
                 num := 4);
            "cc视觉".hmi[12] := 1;
        ELSIF "cc视觉".u_data[1] = '3' THEN
            "发送"(buf := 'fsz_18',
                 num := 4);
            "cc视觉".hmi[13] := 1;
        END_IF;
        "发送"(buf := 'plc_yy_ok',
             num := 1);
    ELSIF "cc视觉".u_data[0] = 'sj_plc_ry' THEN
        IF "cc视觉".u_data[2] = '1988' THEN
            "发送"(buf := 'fry_18',
                 num := 4);
            "cc视觉".u_data[2] := '36';
        ELSIF "cc视觉".u_data[2] = '1998' THEN
            "发送"(buf := 'fry_17',
                 num := 4);
            "cc视觉".u_data[2] := '26';
        ELSIF "cc视觉".u_data[2] = '2008' THEN
            "发送"(buf := 'fry_16',
                 num := 4);
            "cc视觉".u_data[2] := '16';
        ELSIF "cc视觉".u_data[2] = '2018' THEN
            "发送"(buf := 'fry_15',
                 num := 4);
            "cc视觉".u_data[2] := '6';
        END_IF;
        IF "jishu_ry" = 0 THEN
            FOR #i := 0 TO 3 DO
                "cc视觉".r1[#i] := "cc视觉".u_data[#i + 1];
                "cc视觉".wzzl[0] := "cc视觉".r1[2];
                "cc视觉".wzzl[1] := "cc视觉".r1[3];
            END_FOR;
        ELSIF "jishu_ry" = 1 THEN
            FOR #i := 0 TO 3 DO
                "cc视觉".r2[#i] := "cc视觉".u_data[#i + 1];
                "cc视觉".wzzl[2] := "cc视觉".r2[2];
                "cc视觉".wzzl[3] := "cc视觉".r2[3];
            END_FOR;
        ELSIF "jishu_ry" = 2 THEN
            FOR #i := 0 TO 3 DO
                "cc视觉".r3[#i] := "cc视觉".u_data[#i + 1];
                "cc视觉".wzzl[4] := "cc视觉".r3[2];
                "cc视觉".wzzl[5] := "cc视觉".r3[3];
            END_FOR;
        ELSIF "jishu_ry" = 3 THEN
            FOR #i := 0 TO 3 DO
                "cc视觉".r4[#i] := "cc视觉".u_data[#i + 1];
                "cc视觉".wzzl[6] := "cc视觉".r4[2];
                "cc视觉".wzzl[7] := "cc视觉".r4[3];
            END_FOR;
        END_IF;

    ELSIF "cc视觉".u_data[0] = 'sj_plc_wz' THEN
        "发送"(buf := 'plc_tx_wz',
             num := 2);
    END_IF;
END_IF;
——————————————————————
IF "shou4".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "dd机器人".r_data[#i] = ',' OR "dd机器人".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "dd机器人".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "dd机器人".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
            
        END_IF;
    END_FOR;
    "dd机器人".r_data := "dd机器人".e_data;
    IF "dd机器人".u_data[0] = 'jqr_plc_ewm' THEN
        "发送"(buf := 'plc_sj_ewm',
             num := 3);
    ELSIF "dd机器人".u_data[0] = 'jqr_plc_ewm_again' THEN
        "jishu_ewm" += 1;
        IF "jishu_ewm" < 3 THEN
            IF "jishu_ewm" = 1 THEN
                "发送"(buf := 'qwem10',
                     num := 4);
            ELSIF "jishu_ewm" = 2 THEN
                "发送"(buf := 'qewm12',
                     num := 4);
            END_IF;
        ELSE
            "jishu_ewm" := 0;
            "发送"(buf := 'plc_yy_ok',
                 num := 1);
        END_IF;
    ELSIF "dd机器人".u_data[0] = 'jqr_plc_sz' THEN
        "发送"(buf := 'plc_sj_sz',
             num := 3);
    ELSIF "dd机器人".u_data[0] = 'jqr_plc_kb' THEN
        IF "i0.1" THEN
            "发送"(buf := 'fkb_23',
                 num := 4);
            "cc视觉".hmi[21] := 1;
        ELSIF "i0.2" THEN
            "发送"(buf := 'fkb_23',
                 num := 4);
            "cc视觉".hmi[22] := 1;
        ELSIF "i0.3" THEN
            "发送"(buf := 'fkb_23',
                 num := 4);
            "cc视觉".hmi[23] := 1;
        ELSIF "i1.4" THEN
            "发送"(buf := 'fkb_23',
                 num := 4);
            "cc视觉".hmi[24] := 1;
        END_IF;
        "发送"(buf := 'plc_yy_ok',
             num := 1);
    ELSIF "dd机器人".u_data[0] = 'jqr_plc_ry' THEN
        "发送"(buf := 'plc_sj_ry',
             num := 3);
    ELSIF "dd机器人".u_data[0] = 'jqr_plc_ry_again' THEN
        "jishu_ry" += 1;
        IF "jishu_ry" < 4 THEN
            IF "jishu_ry" = 1 THEN
                "发送"(buf := 'qry_04',
                     num := 4);
            ELSIF "jishu_ry" = 2 THEN
                "发送"(buf := 'qry_05',
                     num := 4);
            ELSIF "jishu_ry" = 3 THEN
                "发送"(buf := 'qry_06',
                     num := 4);
            END_IF;
        ELSE
            "jishu_ry" := 0;
            "发送"(buf := 'plc_yy_ok',
                 num := 1);
        END_IF;
    ELSIF "dd机器人".u_data[0] = 'jqr_plc_wz_again' THEN
        "物资发放标志" := 1;
    END_IF;
END_IF;
IF "到位标志" = 0 AND "物资识别" AND "物资发放标志" THEN
    "物资发放标志" := 0;
    "步骤" := 3;
END_IF;
——————————————————————
IF "shou5".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "ee按钮".r_data[#i] = ',' OR "ee按钮".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "ee按钮".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "ee按钮".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
            
        END_IF;
    END_FOR;
    "ee按钮".r_data := "ee按钮".e_data;
    IF "ee按钮".u_data[0] = 'an_plc_zz' THEN
        "步骤" := 1;
    ELSIF "ee按钮".u_data[0] = 'an_plc_fz' THEN
        "步骤" := 2;
    ELSIF "ee按钮".u_data[0] = 'an_plc_wz' THEN
        "物资发放标志" := 1;
    END_IF;
END_IF;
——————————————————————
"发送长度" := LEN(#buf);
IF #num = 1 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "aa语音".s_data);
    "发送标志" := 1;
ELSIF #num = 2 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "bb图像".s_data);
    "发送标志" := 1;
ELSIF #num = 3 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "cc视觉".s_data);
    "发送标志" := 1;
ELSIF #num = 4 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "dd机器人".s_data);
    "发送标志" := 1;
END_IF;