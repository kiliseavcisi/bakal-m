# "Tahta" (whiteboard) for the Albanian app. Method: we shorten Turkish when we speak; write the FULL Turkish back,
# then match every piece one-to-one with the Albanian piece. The teacher (Ava HD) speaks Turkish; every Albanian
# word in the narration is written «like this» and is read by Anila inside the same clip.
# Step: (narration, rows, Albanian sentences played after the narration, clear board first)
# Rows: [x] dropped in spoken Turkish  ~x~ crossed out  {x} key piece  *x* Albanian (blue)  -> arrow
#       "=tr|sq · tr|sq" one-to-one coloured pairs
BOARDS_SQ = {
 "p-oj": [
  ("Çalışıyorum. Tam hâli, ben çalışıyorum. Kim çalışıyor? Ben. Türkçe bunu sondaki um ekine saklar.",
   ["Çalışıyorum.", "[Ben] çalış-ıyor-{um}"], [], False),
  ("Arnavutça da saklar, tıpkı Türkçe gibi. Ben kelimesini söylemeden «punoj» dersin. «Puno», çalış demek. Sondaki j, ben demek.",
   ["=çalış|puno · -ıyor-um (ben)|-j"], ["punoj"], False),
  ("Kişi değişince sadece son değişir, Türkçedeki gibi. Çalışıyorsun, «punon». Çalışıyoruz, «punojmë». Çalışıyorlar, «punojnë».",
   ["=çalışıyor|puno · -um|-j", "=çalışıyor|puno · -sun|-n", "=çalışıyor|puno · -uz|-jmë", "=çalışıyor|puno · -lar|-jnë"], ["Ne punojmë.", "Ata punojnë."], True),
  ("Bir fark var. Arnavutçada şimdiki zamanla geniş zaman aynıdır. «Punoj», hem çalışıyorum, hem çalışırım demek. Türkçedeki iki eki tek ek karşılar.",
   ["çalışıyorum / çalışırım -> *punoj*"], [], True)],
 "p-shkuar": [
  ("Çalıştım. Tam hâli, ben çalıştım. İki ek var. Tı, geçmiş demek. M, ben demek.",
   ["Çalıştım.", "[Ben] çalış-{tı}-{m}"], [], False),
  ("Arnavutça da iki parça kullanır: «punova». «Puno», çalış. V, geçmiş. A, ben.",
   ["=çalış|puno · -tı (geçmiş)|-v · -m (ben)|-a"], ["punova"], False),
  ("Sen çalıştın, «punove». O çalıştı, «punoi». Biz çalıştık, «punuam». Sondaki parça kişiyi söyler, tam Türkçe gibi.",
   ["=çalış|puno · -tı|-v · -m|-a", "=çalış|puno · -tı|-v · -n|-e", "=çalış|puno · -tı (o)|-i", "=çalış|punu · -tı-k|-am"], [], True),
  ("En çok kullanılan fiiller ise kökünden değişir. Gitmek «shkoj», gittim «shkova». Ama gelmek «vij», geldim «erdha». Yemek «ha», yedim «hëngra». Bunlar az, kelime gibi ezberle.",
   ["shkoj -> *shkova*", "vij -> *erdha* (!)", "ha -> *hëngra* (!)"], ["shkova", "erdha", "hëngra"], True)],
 "p-dote": [
  ("Çalışacağım. Tam hâli, ben çalışacağım. Acak eki gelecek demek, ım de ben.",
   ["Çalışacağım.", "[Ben] çalış-{acağ}-ım"], [], False),
  ("Arnavutça gelecek ekini fiilin önüne koyar: «do të». Gerisi bildiğin şimdiki zaman. «Do të punoj».",
   ["=-acak|do të · çalış|puno · -ım (ben)|-j"], ["Do të punoj."], False),
  ("«Do», aslında istemek fiilinden gelir. Yani Arnavut, geleceği, istiyor ki çalışayım diye kurar. Kişi değişince yine sadece son değişir.",
   ["=-acak|do të · çalış|puno · -sın|-sh", "=-acak|do të · çalış|puno · (o)|-jë", "=-acağ|do të · çalış|puno · -ız|-jmë"], ["Nesër do të punoj."], True),
  ("Olumsuzda «nuk», «do»nun önüne gelir. «Nuk do të vij». Gelmeyeceğim.",
   ["=-me|nuk · -yecek|do të · gel-im|vij"], ["Nuk do të vij."], False)],
 "p-pakryer": [
  ("Türkçede geçmişte süren iş için iki ek var: çalışıyordum ve çalışırdım. Arnavutça ikisine tek biçim kullanır: «punoja».",
   ["çalışıyordum / çalışırdım -> *punoja*"], ["punoja"], False),
  ("Parçalara bakalım. «Puno», çalış. Ja, hem geçmişte sürüyordu, hem ben demek.",
   ["=çalış|puno · -ıyordu/-ırdı + -m|-ja"], [], False),
  ("Peki ne zaman «punova», ne zaman «punoja»? Kendine sor. Bir kere olup bitti mi? «Punova». Sürüyor muydu, ya da tekrarlanıyor muydu? «Punoja».",
   ["bir kere, bitti -> *punova* (çalıştım)", "sürüyordu / alışkanlık -> *punoja* (çalışırdım)"], ["Dje punova.", "Dikur punoja shumë."], True),
  ("O sırada demek için önüne «po» koyarsın. «Kur erdhe, unë po haja». Sen geldiğinde, ben yemek yiyordum.",
   ["=sen geldiğinde|kur erdhe · ben|unë · yiyordum|po haja"], ["Kur erdhe, unë po haja."], True)],
 "p-kam-qene": [
  ("Tiran'da bulundum. Arnavutça bunu, Tiran'da bulunmuşluğa sahibim diye kurar. Garip gelir ama mantığı bu.",
   ["Tiran'da bulundum.", "[Ben] Tiran'da {bulunmuş}[luğa sahibim]."], [], False),
  ("Birebir: «kam», sahibim. «Qenë», bulunmuş. «Në Tiranë», Tiran'da.",
   ["=sahibim|kam · bulunmuş|qenë · Tiran'da|në Tiranë"], ["Kam qenë në Tiranë."], False),
  ("Kişi değişince sadece «kam» değişir: «ke», «ka». Ortaç hep aynı kalır. Hiç Kosova'da bulundun mu?",
   ["=sen sahipsin|ke · bulunmuş|qenë · hiç|ndonjëherë"], ["A ke qenë ndonjëherë në Kosovë?"], True),
  ("Ne zaman «punova», ne zaman «kam punuar»? Ne zaman olduğu önemliyse, dün gibi, «punova». Önemli olan sonuçsa ya da deneyimse, «kam punuar».",
   ["dün, geçen yıl -> *punova*", "hiç, şimdiye kadar, henüz -> *kam punuar*"], ["Nuk kam ngrënë ende."], True)],
 "p-nese": [
  ("Vaktin varsa gel. Bu gerçek bir şart. Tam hâli, eğer vaktin varsa, gel. Eğer, «nëse» olur ve başa gelir.",
   ["Vaktin varsa gel.", "[Eğer] vakt-in var-{sa}, gel.", "=eğer -sa|nëse · vaktin var|ke kohë · gel|eja"], ["Nëse ke kohë, eja!"], False),
  ("Hayali şart başka. Param olsaydı, ev alırdım. «Po të kisha», sahip olsaydım. «Do të blija», alırdım.",
   ["=olsaydı (sahip olsaydım)|po të kisha · para|para", "=alırdım|do të blija · bir ev|një shtëpi"], ["Po të kisha para, do të blija një shtëpi."], True),
  ("Bak, Türkçedeki ırdı, Arnavutçada gelecek ekiyle eskiden ekinin birleşimi: «do të», artı ja. Alacaktım gibi düşün.",
   ["=al|blij · -ır-dı (-acaktı)|do të … -a"], ["Do të doja një kafe."], True)],
 "p-mund": [
  ("Gelebilirim. Türkçede ebil eki fiilin içinde.", ["Gelebilirim.", "[Ben] gel-{ebil}-ir-im"], [], False),
  ("Arnavutça bunu ayrı kelimeyle söyler: «mund të». Sonra fiil, kişiye göre.",
   ["=-ebil-|mund të · gel-ir-im|vij"], ["Mund të vij."], False),
  ("Gerekmek için «duhet të». Gitmeliyim, «duhet të iki». Aradaki «të», Türkçedeki mek eki gibi iki fiili bağlar. Gitmek istiyorum, «dua të shkoj».",
   ["=-meli-|duhet të · git-im|iki", "=git-mek istiyorum|dua të shkoj"], ["Duhet të iki.", "Dua të mësoj më shumë."], True)],
 "p-kisha": [
  ("Tren kalkmıştı. Türkçede mış ve tı birleşir: önceden olmuş, ve geçmişte. Arnavutça bunu sahiptim fiiliyle kurar.",
   ["Tren kalkmıştı.", "Tren kalk-{mış}-{tı}."], [], False),
  ("«Kisha ngrënë», yemiştim. «Kisha», sahiptim. «Ngrënë», yemiş. Yani, yemişliğe sahiptim.",
   ["=sahiptim|kisha · yemiş|ngrënë"], ["Kisha ngrënë kur erdhe."], True),
  ("Bazı fiillerde sahip olmak yerine olmak gelir. «Ishte nisur», kalkmış idi.",
   ["=idi|ishte · kalkmış|nisur"], ["Treni ishte nisur."], False)],
 "p-qenka": [
  ("Güzelmiş! Türkçede mış eki şaşırmayı da anlatır. Arnavutçada bunun için ayrı bir biçim var.",
   ["Güzel-{miş}!"], [], False),
  ("«Qenka», imiş demek. «Qenka shumë e bukur», çok güzelmiş.",
   ["=imiş|qenka · çok güzel|shumë e bukur"], ["Qenka shumë e bukur!"], False),
  ("Fiillerde sona ka ya da ke eklenir. «Flitke», konuşuyormuşsun. «Paske ardhur», gelmişsin.",
   ["=konuşuyor-muş-sun|flit-ke", "=gelmiş-sin|paske ardhur"], ["Ti flitke shqip!", "Paske ardhur!"], True)],
 "p-pelqen": [
  ("Elmayı severim. Türkçede seven benim. Arnavutça olaya ters bakar: elma bana hoş gelir.",
   ["Elmayı severim.", "[Ben] elma-yı sev-er-im."], [], False),
  ("Arnavutça düşünceyle Türkçesi: bana hoş gelir elma. Birebir: «më», bana. «Pëlqen», hoş gelir. «Molla», elma.",
   ["Bana hoş gelir [o] elma.", "=bana|më · hoş gelir|pëlqen · elma|molla"], ["Më pëlqen molla."], True),
  ("Elma özne olduğu için, elmalar dersen fiil çoğul olur. Bana hoş gelirler armutlar: «më pëlqejnë dardhat».",
   ["=bana|më · hoş gelirler|pëlqejnë · armutlar|dardhat"], ["Më pëlqejnë dardhat."], True)],
 "p-dhemb": [
  ("Başım ağrıyor. Türkçede ağrıyan baş, ama başın kimin olduğunu ım eki söyler.",
   ["Baş-{ım} ağrıyor."], [], False),
  ("Arnavutça der ki: bana ağrıyor baş. Birebir: «më», bana. «Dhemb», ağrıyor. «Koka», o baş.",
   ["Bana ağrıyor [o] baş.", "=bana|më · ağrıyor|dhemb · baş|koka"], ["Më dhemb koka."], True),
  ("Ağrıyan çoğulsa fiil de çoğul olur. Bana ağrıyorlar bacaklar: «më dhembin këmbët».",
   ["=bana|më · ağrıyorlar|dhembin · bacaklar|këmbët"], ["Më dhembin këmbët."], True)],
}
