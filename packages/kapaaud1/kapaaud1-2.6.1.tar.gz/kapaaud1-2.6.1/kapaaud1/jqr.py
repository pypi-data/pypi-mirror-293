if data=="plc_q2a" then
      yd(P2,1)
      yd(P14,0)
      Go(P1)
      TCPWrite(socket,"fw")
    elsif data=="plc_q3a" then
      yd(P3,1)
      yd(P14,0)
      Go(P1)
      TCPWrite(socket,"fw")
    elsif data=="plc_q4a" then
      yd(P4,1)
      yd(P14,0)
      Go(P1)
      TCPWrite(socket,"fw")
    elsif data=="plc_q5a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elsif data=="plc_q6a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elsif data=="plc_q7a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elsif data=="plc_q8a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elseif data=="plc_q9a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elseif data=="plc_q10a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elseif data=="plc_q11a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elseif data=="plc_q12a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elseif data=="plc_q13a" then
      yd(P5,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"fw")
    elseif data=="f1" then
      yd(P14,1)
      yd(P16,0)
      Go(P1)
      TCPWrite(socket,"js")
    elseif data=="f2" then
      yd(P14,1)
      yd(P17,0)
      Go(P1)
      TCPWrite(socket,"js")
    elseif data=="f3" then
      yd(P14,1)
      yd(P18,0)
      Go(P1)
      TCPWrite(socket,"js")
    elseif data=="f4" then
      yd(P14,1)
      yd(P19,0)
      Go(P1)
      TCPWrite(socket,"js")
    elseif data=="f5" then
      yd(P14,1)
      yd(P16,0)
      Go(P1)
      TCPWrite(socket,"js")
    elseif data=="f6" then
      yd(P14,1)
      yd(P17,0)
      Go(P1)
      TCPWrite(socket,"js")
    elseif data=="f7" then
      yd(P14,1)
      yd(P18,0)
      Go(P1)
      TCPWrite(socket,"js")
    elseif data=="f8" then
      yd(P14,1)
      yd(P19,0)
      Go(P1)
      TCPWrite(socket,"js")
    elseif data=="plc_bz1_zfsb" then
      yd(P9,1)
      yd(P14,0)
      Go(P1)
      TCPWrite(socket,"ok")
    elseif data=="plc_bz1_wzff_a" then
      yd(P12,1)
      yd(P14,0)
      Go(P1)
      TCPWrite(socket,"ok") 
    elseif data=="plc_bz1_wzff_b" then
      yd(P9,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"ok") 
    elseif data=="plc_bz1_wzff_c" then
      yd(P11,1)
      yd(P14,0)
      Go(P1)
    TCPWrite(socket,"ok") 
     elseif data=="plc_bz1_wzff_d" then
      yd(P8,1)
      yd(P14,0)
      Go(P1)
      TCPWrite(socket,"ok") 
    elseif data=="A" then
      yd(P14,1)
      yd(P19,1)
      Go(P1)
      TCPWrite(socket,"ok")
    elseif data=="B" then
      yd(P14,1)
      yd(P19,1)
      Go(P1)
      TCPWrite(socket,"ok")
    elseif data=="plc_bz1_kb" then
      yd(P13,1)
      yd(P15,0)
      Go(P1)
      TCPWrite(socket,"ok")
    elseif data=="plc_kb_fng" then
      yd(P15,1)
      yd(P24,0)
      Go(P1)
      TCPWrite(socket,"ok")  
    end