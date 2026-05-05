def interpret_features(features):
    """
    Stage 6: Rule-based Feature Interpretation
    Maps extracted features to interpretive labels using predefined thresholds.
    This is framed as an entertainment-layer output.
    """
    print("[Stage 6] Interpreting features based on physiognomy rules")
    
    interpretation = {"face": [], "eye": [], "lip": []}
    
    # ---------------------------
    # Face Interpretation
    # ---------------------------
    L = features["face"]["L"]
    J = features["face"]["J"]
    F = features["face"]["F"]
    forehead_w = features["face"]["forehead_w"]
    cheek_w = features["face"]["cheek_w"]
    jaw_w = features["face"]["jaw_w"]
    diff = features["face"]["symmetry_diff"]
    
    shape = "Mặt oval"
    if L > 1.58: shape = "Mặt dài"
    elif L < 1.30 and J > 0.88: shape = "Mặt tròn"
    elif L < 1.40 and J > 0.95: shape = "Mặt vuông"
    elif F > 1.03 and J < 0.84: shape = "Mặt trái tim"
    elif F < 0.94 and J > 0.95: shape = "Mặt tam giác"
    elif cheek_w > forehead_w and cheek_w > jaw_w and J < 0.88: shape = "Mặt kim cương"
    interpretation["face"].append(f"Hình dáng: {shape}")
    
    if J < 0.78: jaw = "Jawline V-line"
    elif J < 0.92: jaw = "Jawline thon"
    else: jaw = "Jawline rộng"
    interpretation["face"].append(jaw)
    
    if cheek_w > forehead_w*1.05 and cheek_w > jaw_w*1.05: cheek = "Gò má nổi bật"
    else: cheek = "Gò má mềm"
    interpretation["face"].append(cheek)
    
    if diff < 22: sym = "Rất cân đối"
    elif diff < 35: sym = "Khá cân đối"
    else: sym = "Lệch nhẹ"
    interpretation["face"].append(f"Độ cân xứng: {sym}")

    # ---------------------------
    # Eye Interpretation
    # ---------------------------
    ratio = features["eye"]["ratio"]
    tilt = features["eye"]["tilt"]
    gap_ratio = features["eye"]["gap_ratio"]
    horizontal_score = features["eye"]["horizontal_score"]
    eye_height = features["eye"]["eye_height"]
    
    eye_shape = "Mắt cân đối"
    if ratio > 0.36: eye_shape = "Mắt tròn"
    elif ratio < 0.26: eye_shape = "Mắt hạnh nhân"
    interpretation["eye"].append(eye_shape)
    
    if tilt < -4: interpretation["eye"].append("Mắt xếch")
    elif tilt > 4: interpretation["eye"].append("Mắt sụp")
    
    if gap_ratio < 0.22: interpretation["eye"].append("Mắt gần nhau")
    elif gap_ratio > 0.30: interpretation["eye"].append("Mắt xa nhau")
    
    eyelid = "Một mí / mí ẩn"
    if horizontal_score > 220: eyelid = "Hai mí rõ"
    elif horizontal_score > 130: eyelid = "Mí lót"
    interpretation["eye"].append(eyelid)
    
    if ratio > 0.40 and eye_height > 18: interpretation["eye"].append("Mắt lồi nhẹ")

    # ---------------------------
    # Lip Interpretation
    # ---------------------------
    lip_ratio = features["lip"]["lip_ratio"]
    tb_ratio = features["lip"]["tb_ratio"]
    bow_depth = features["lip"]["bow_depth"]
    
    if lip_ratio < 0.22: interpretation["lip"].append("Môi mỏng")
    elif lip_ratio < 0.30: interpretation["lip"].append("Môi vừa")
    else: interpretation["lip"].append("Môi đầy")
    
    if tb_ratio > 1.15: interpretation["lip"].append("Môi trên dày hơn")
    elif tb_ratio < 0.85: interpretation["lip"].append("Môi dưới dày hơn")
    else: interpretation["lip"].append("Hai môi cân đối")
    
    if bow_depth > 7: interpretation["lip"].append("Môi trái tim / Cupid bow rõ")
    elif bow_depth > 4: interpretation["lip"].append("Cupid bow nhẹ")
    else: interpretation["lip"].append("Viền môi tròn")

    return interpretation
