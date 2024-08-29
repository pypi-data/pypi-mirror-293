class STWeights:
    def __init__(self):
        # Regular expression patterns for identifying start and end word sequences
        self.start_re_patterns = [
            r"(?<= )\b[A-Z]\.(?= )",
            r"(?<= )\b[A-Z][a-z]\.(?= )"
        ]
        self.end_re_patterns = []

        # Characters likely to appear at the start or end of words
        self.start_chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789*#@$%^&([{+!-=:;<>~')
        self.end_chars = list('!.؟。٬:;’"’…‽⁇⁈⁉⸮⸼꓿꘎꘏꛳꛷꡶꡷꣎꣏꤯꧈꧉꩝꩞꩟꫰꫱꯫﹒﹖﹗！．？𐩖𐩗𑁇𑁈𑂾𑂿𑃀𑃁𑅁𑅂𑅃𑇅𑇆𑇍𑇞𑇟𑈸𑈹𑈻𑈼𑊩𑑋𑑌𑗂𑗃𑗉𑗊𑗋𑗌𑗍𑗎𑗏𑗐𑗑𑗒𑗓𑗔𑗕𑙁𑙂𑜼𑜽𑜾𑩂𑩃𪛛𪜜𱁁𱂂𖩮𖩯𖫵𖬷𖬸𖭄𛲟𝪈｡。')

        # Common start and end words used for segmentation and sentence boundary detection
        self.start_words = [
            'Dr.', 'Sr.', 'Jr.', 'Mrs.', 'Mr.', 'Ms.', 'Prof.', 'Inc.', 'Ltd.', 'Co.', 'e.g.', 'i.e.', 
            'U.S.', 'A.D.', 'B.C.', 'Drs.', 'Ph.D.', 'St.', 'the', 'a', 'an', 'this', 'that', 'there', 
            'it', 'he', 'she', 'we', 'they', 'i', 'you', 'as', 'if', 'because', 'when', 'where', 'why', 
            'how', 'who', 'which', 'what', 'some', 'many', 'each', 'every', 'all', 'most', 'few', 
            'several', 'one', 'two', 'three', 'first', 'next', 'then', 'after', 'before', 'during', 
            'until', 'while', 'since', 'despite', 'although', 'both', 'neither', 'either', 'even', 'so'
        ]
        self.end_words = [
            'end', 'final', 'conclusion', 'thus', 'therefore', 'hence', 'afterwards', 'later', 
            'finally', 'ultimately', 'in conclusion', 'overall', 'however', 'nevertheless', 
            'nonetheless', 'meanwhile', 'besides', 'also', 'instead', 'consequently', 'subsequently', 
            'briefly', 'in summary', 'in short', 'to summarize', 'nonetheless', 'accordingly', 'thus', 
            'thereafter'
        ]

        # Weights (from 0 to 1) for various probabilities in sentence boundary detection
        self.pro_first_word_weight = 1.0
        self.pro_last_word_weight = 1.0
        self.pro_start_char_mask_weight = 0.4
        self.pro_end_char_mask_weight = 0.4
        self.pro_start_word_mask_weight = 0.3
        self.pro_end_word_mask_weight = 0.3

        # Advanced weight settings for probability adjustments based on context
        self.prob_first_add_prev_prob_last_gte_condi_weight = 0.4
        self.prob_first_add_prev_prob_last_gte_val_weight = 0.3
        self.prob_first_sub_prev_prob_first_gt_prob_first_val_weight = 0.1
        self.prob_first_sub_next_prob_first_gt_prob_first_val_weight = 0.1
        self.prob_first_sub_next_prob_last_gt_prob_first_val_weight = 0.1

        self.prob_last_add_next_prob_first_gte_condi_weight = 0.4
        self.prob_last_add_next_prob_first_gte_val_weight = 0.3
        self.prob_last_sub_next_prob_last_gt_prob_last_val_weight = 0.1
        self.prob_last_sub_prev_prob_first_gt_prob_last_val_weight = 0.1
        self.prob_last_sub_prev_prob_last_gt_prob_last_val_weight = 0.1

        self.prob_last_sub_prob_first_gte_prob_last_val_weight = 0.2
        self.prob_first_sub_prob_last_gte_prob_first_val_weight = 0.2
