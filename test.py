pattern_en_pr = r'\s*([a-zA-Z\.\s*]+)\.\s*([0-9]+)\.\s*“(.*?)”\.\s*In(.*?)\s*\(ed(.*?)\),\s*(.*?)\.\s*(.*?):\s*(.*?)\.\s*(.*?)\.\s*(.*?)\.\s*'#proceedings
pattern_en_pr_noad = r'\s*([a-zA-Z\.\s*]+)\.\s*([0-9]+)\.\s*“(.*?)”\.\s*In(.*?)\s*\(ed(.*?)\),\s*(.*?)\.\s*(.*?)\.\s*(.*?)\.\s*(.*?)\.\s*'#无出版地proceedings
pattern_en_b = r'\s*([a-zA-Z\.\s*]+)\.\s*([0-9]+)\.\s*(.*?)\.\s*(.*?):(.*?)\.\s*'#books
pattern_en_b_noad = r'\s*([a-zA-Z\.\s*]+)\.\s*([0-9]+)\.\s*(.*?)\.\s*(.*?)\.\s*'#无出版地books
pattern_en_ar = r'\s*([a-zA-Z\.\s*]+)\.\s*([0-9]+)\.\s*“(.*?)”\.(.*?)\.\s*(.*?)\((.*?)\)\.\s*pp\.(.*?)\-+(.*?)\.\s*'#article
pattern_en_ar_nonum = r'\s*([a-zA-Z\.\s*]+)\.\s*([0-9]+)\.\s*“(.*?)”\.(.*?)\.\s*(.*?):pp\.(.*?)\-+(.*?)\.\s*'#无number article