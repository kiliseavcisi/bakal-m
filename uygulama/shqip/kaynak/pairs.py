# Minimal pairs for perceptual (HVPT-style) training: contrasts that are hard for Turkish speakers.
# (id, label, how-to tip, [(word_a, tr_a), (word_b, tr_b)] pairs)
PAIRS = [
 ("q-c", "q – ç", "<b>q</b> dilin ortası damağa değer, yumuşak bir ç; <b>ç</b> Türkçedeki gibi.", [(("qaj", "ağlıyorum"), ("çaj", "çay")), (("qetë", "sakin"), ("çetë", "çete"))]),
 ("th-dh", "th – dh", "<b>th</b> sessizdir (İng. <i>think</i>), <b>dh</b> sesli (İng. <i>this</i>). Dil dişlerin arasında.", [(("thi", "domuz"), ("dhi", "keçi"))]),
 ("rr-r", "rr – r", "<b>rr</b> dil ucu birkaç kez titreşir; <b>r</b> tek dokunuş.", [(("ara", "tarla"), ("arra", "cevizler")), (("bari", "çimen"), ("barri", "yük"))]),
 ("ll-l", "ll – l", "<b>ll</b> kalın l (Türkçe <i>oldu</i>); <b>l</b> ince (Türkçe <i>lale</i>).", [(("mal", "dağ"), ("mall", "özlem")), (("hala", "hâlâ"), ("halla", "hala (akraba)"))]),
 ("e-ë", "e – ë", "<b>ë</b> kısa, ı ile ö arası; <b>e</b> açık e. Kelime sonundaki ë çoğu zaman duyulmaz.", [(("ne", "biz"), ("në", "-de/-da")), (("le", "izin ver"), ("lë", "bırak"))]),
 ("nj-n", "nj – n", "<b>nj</b> İspanyolca ñ gibi (ny); <b>n</b> düz n.", [(("një", "bir"), ("në", "-de/-da"))]),
 ("gj-xh", "gj – xh", "<b>gj</b> dil damakta, yumuşak c; <b>xh</b> Türkçedeki c.", [(("gjel", "horoz"), ("xhel", "jöle"))]),
 ("y-i", "y – i", "<b>y</b> Türkçedeki ü; <b>i</b> Türkçedeki i.", [(("dy", "iki"), ("di", "bilir")), (("sy", "göz"), ("si", "nasıl"))]),
]
