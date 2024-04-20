class config:
    serial_port = "/dev/ttyUSB0"
    serial_baudrate = 2400
    serial_timeout = 2
    update_interval = 60
    devices = [0, 1, 2]
    trim_result = 3
    data_key_timestr = "zeit"
    data_key_time_num = "zeit_num"
    data_key_device = "geraet"
    data_keys = [
        ("startseq", "str"),  # (A
        ("serialnum", "int"),  # BBBBBBBBBBBBBB
        ("modus", "str"),  # C
        ("fehlercode", "int"),  # DD
        ("v_ac_eingang", "float"),  # EEE.E
        ("f_ac_eingang", "float"),  # FF.FF
        ("v_ac_ausgang", "float"),  # GGG.G
        ("f_ac_ausgang", "float"),  # HH.HH
        ("s_ac_ausgang", "float"),  # IIII
        ("p_ac_ausgang", "float"),  # JJJJ
        ("p_prozent_ausgang", "float"),  # KKK
        ("v_batterie", "float"),  # LL.L
        ("i_batterie_laden", "float"),  # MMM
        ("prozent_batterie", "float"),  # NNN
        ("v_pv_eingang", "float"),  # OOO.O
        ("i_laden_gesamt", "float"),  # PPP
        ("s_ac_ausgang_gesamt", "float"),  # QQQQQ
        ("p_ac_ausgang_gesamt", "float"),  # RRRRR
        ("p_prozent_ausgang", "float"),  # SSS
        ("inverter_status", "str"),  # b7b6b5b4b3b2b1b0
        ("ac_ausgang_modus", "int"),  # T
        ("batterie_laden_prio", "int"),  # U
        ("i_max_laden_einstellung", "float"),  # VVV
        ("i_max_ladenmoeglich", "float"),  # WWW
        ("i_max_laden_ac", "float"),  # XX
        ("i_pv_eingang", "float"),  # YY.Y
        ("i_batterie_entladen", "float"),  # ZZZ
    ]
    data_folder = "data"
    data_filename = "%y%m%d.tsv"
