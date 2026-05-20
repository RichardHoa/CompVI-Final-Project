def interpret_features(features):
    """
    Stage 6: Rule-based Feature Interpretation
    Maps extracted features to interpretive labels using predefined thresholds.
    This is framed as an entertainment-layer output.
    """
    print("[Stage 6] Interpreting features based on physiognomy rules")
    
    interpretation = {"face": [], "eye": [], "lip": [], "thirds": [], "nose": []}
    
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
    
    shape = "Oval face"
    if L > 1.58: shape = "Long face"
    elif L < 1.30 and J > 0.88: shape = "Round face"
    elif L < 1.40 and J > 0.95: shape = "Square face"
    elif F > 1.03 and J < 0.84: shape = "Heart face"
    elif F < 0.94 and J > 0.95: shape = "Triangle face"
    elif cheek_w > forehead_w and cheek_w > jaw_w and J < 0.88: shape = "Diamond face"
    interpretation["face"].append(f"Shape: {shape}")
    
    if J < 0.78: jaw = "V-line jawline"
    elif J < 0.92: jaw = "Slim jawline"
    else: jaw = "Wide jawline"
    interpretation["face"].append(jaw)
    
    if cheek_w > forehead_w*1.05 and cheek_w > jaw_w*1.05: cheek = "Prominent cheekbones"
    else: cheek = "Soft cheekbones"
    interpretation["face"].append(cheek)
    
    if diff < 22: sym = "Very symmetric"
    elif diff < 35: sym = "Fairly symmetric"
    else: sym = "Slightly asymmetric"
    interpretation["face"].append(f"Symmetry: {sym}")

    # ---------------------------
    # Eye Interpretation
    # ---------------------------
    ratio = features["eye"]["ratio"]
    tilt = features["eye"]["tilt"]
    gap_ratio = features["eye"]["gap_ratio"]
    horizontal_score = features["eye"]["horizontal_score"]
    eye_height = features["eye"]["eye_height"]
    
    eye_shape = "Proportional eyes"
    if ratio > 0.36: eye_shape = "Round eyes"
    elif ratio < 0.26: eye_shape = "Almond eyes"
    interpretation["eye"].append(eye_shape)
    
    if tilt < -4: interpretation["eye"].append("Upturned eyes")
    elif tilt > 4: interpretation["eye"].append("Downturned eyes")
    
    if gap_ratio < 0.22: interpretation["eye"].append("Close-set eyes")
    elif gap_ratio > 0.30: interpretation["eye"].append("Wide-set eyes")
    
    eyelid = "Monolid / hooded"
    if horizontal_score > 220: eyelid = "Double eyelids"
    elif horizontal_score > 130: eyelid = "Hidden double eyelids"
    interpretation["eye"].append(eyelid)
    
    if ratio > 0.40 and eye_height > 18: interpretation["eye"].append("Slightly protruding eyes")

    # ---------------------------
    # Lip Interpretation
    # ---------------------------
    lip_ratio = features["lip"]["lip_ratio"]
    tb_ratio = features["lip"]["tb_ratio"]
    bow_depth = features["lip"]["bow_depth"]
    
    if lip_ratio < 0.22: interpretation["lip"].append("Thin lips")
    elif lip_ratio < 0.30: interpretation["lip"].append("Medium lips")
    else: interpretation["lip"].append("Full lips")
    
    if tb_ratio > 1.15: interpretation["lip"].append("Thicker upper lip")
    elif tb_ratio < 0.85: interpretation["lip"].append("Thicker lower lip")
    else: interpretation["lip"].append("Proportional lips")
    
    if bow_depth > 7: interpretation["lip"].append("Heart-shaped / prominent Cupid's bow")
    elif bow_depth > 4: interpretation["lip"].append("Subtle Cupid's bow")
    else: interpretation["lip"].append("Rounded lip border")

    # ---------------------------
    # Thirds Interpretation
    # ---------------------------
    upper_ratio = features["thirds"]["upper_ratio"]
    middle_ratio = features["thirds"]["middle_ratio"]
    lower_ratio = features["thirds"]["lower_ratio"]
    balance_score = features["thirds"]["balance_score"]
    
    def classify_third(ratio, name):
        if ratio > 0.38: return f"{name}: slightly long"
        elif ratio < 0.28: return f"{name}: slightly short"
        else: return f"{name}: proportional"
        
    interpretation["thirds"].append(classify_third(upper_ratio, "Upper third"))
    interpretation["thirds"].append(classify_third(middle_ratio, "Middle third"))
    interpretation["thirds"].append(classify_third(lower_ratio, "Lower third"))
    
    if balance_score > 0.82: interpretation["thirds"].append("Face ratio: fairly proportional")
    elif balance_score > 0.68: interpretation["thirds"].append("Face ratio: relatively balanced")
    else: interpretation["thirds"].append("Face ratio: slightly unbalanced")

    # ---------------------------
    # Nose Interpretation
    # ---------------------------
    width_ratio = features["nose"]["width_ratio"]
    length_ratio = features["nose"]["length_ratio"]
    tip_ratio = features["nose"]["tip_ratio"]
    bridge_projection = features["nose"]["bridge_projection"]
    tip_offset = features["nose"]["tip_offset"]
    
    if width_ratio > 0.44: interpretation["nose"].append("Nose wings: slightly wide")
    elif width_ratio > 0.35: interpretation["nose"].append("Nose wings: proportional")
    else: interpretation["nose"].append("Nose wings: narrow")
    
    if length_ratio > 0.34: interpretation["nose"].append("Nose length: slightly long")
    elif length_ratio > 0.24: interpretation["nose"].append("Nose length: average")
    else: interpretation["nose"].append("Nose length: slightly short")
    
    if tip_ratio > 0.95: interpretation["nose"].append("Nose tip: soft round")
    elif tip_ratio > 0.78: interpretation["nose"].append("Nose tip: proportional")
    else: interpretation["nose"].append("Nose tip: defined/narrow")
    
    if tip_offset > 10: interpretation["nose"].append("Nose angle: slightly upturned")
    elif tip_offset < -10: interpretation["nose"].append("Nose angle: slightly downturned")
    else: interpretation["nose"].append("Nose angle: neutral / straight")
    
    if bridge_projection > 0.13: interpretation["nose"].append("Nose bridge: prominent")
    elif bridge_projection > 0.07: interpretation["nose"].append("Nose bridge: natural")
    else: interpretation["nose"].append("Nose bridge: soft / low")

    return interpretation
