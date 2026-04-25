def interpret_features(features):
    """
    Stage 6: Rule-based Feature Interpretation
    Maps extracted features to interpretive labels using predefined thresholds.
    This is framed as an entertainment-layer output.
    """
    print("[Stage 6] Interpreting features based on physiognomy rules")
    
    interpretation = []
    
    if features["face_ratio"] > 1.4:
        interpretation.append("High face ratio indicates an analytical and deliberate thinker.")
    else:
        interpretation.append("Lower face ratio indicates a practical and action-oriented individual.")
        
    if features["jaw_angle"] > 110:
        interpretation.append("A strong jaw angle suggests decisiveness and strong willpower.")
        
    return interpretation
