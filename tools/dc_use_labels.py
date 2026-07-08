#!/usr/bin/env python3
"""In-context (Claude-judgment) land-use classification of DC provisions.

Each DC provision's Purpose statement (from ``data/dc_provisions_text.csv``,
produced by ``tools/extract_dc_uses.py``) was read and assigned ONE dominant
land-use category matching the diversity analysis's DEV categories:

    res / com / ind / mix / inst        (+ ``unknown`` for empties/garbage)

Classification rules (applied consistently — this is the point of in-context
vs keyword matching):
  * "business employment" / "industrial business" / general-light-medium
    industrial / warehousing / manufacturing / waste  -> ind
  * general business / office / retail / shopping centre / highway|convenience
    commercial / hotel / auto dealership / personal service / gas bar / funeral
    (no cemetery) / small health-services clinic                       -> com
  * housing of any kind (single/semi/row/multi/apartment, seniors *housing*,
    group homes); "residential with limited/ancillary commercial"      -> res
  * genuine co-equal two-use (mixed-use, commercial ground floor +
    residential above, TOD urban village)                              -> mix
  * care facilities (nursing home, auxiliary hospital, continuing/extended
    care, assisted living, hospice); religious assembly; schools;
    civic (police/ambulance/fire); cultural centres; recreation/parks;
    utilities; cemeteries; prisons; museums                            -> inst
  * empties/garbage: labelled from slug where unambiguous (condo/homes ->
    res lo; plaza/office-building -> com lo; seniors-centre -> inst lo),
    else unknown. Everything slug-derived gets confidence ``l``.

confidence: h = single clear use; m = clear primary with secondary uses;
            l = ambiguous, slug-derived, or no purpose text.

Run to (re)generate ``data/dc_inferred_use.csv``. Asserts every slug in
``dc_provisions_text.csv`` has exactly one label (no silent drops).
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEXT_CSV = os.path.join(ROOT, "data", "dc_provisions_text.csv")
OUT_CSV = os.path.join(ROOT, "data", "dc_inferred_use.csv")

VALID_USES = {"res", "com", "ind", "mix", "inst", "unknown"}
VALID_CONF = {"h", "m", "l"}

# One line per slug: "slug<TAB>use<TAB>conf[<TAB>note]". Split into chunks
# purely for authoring; concatenated below.
_P1 = """
368-dcind-direct-controlindustrial-district	ind	h
dc-182	com	h
dc-20712	mix	h
dc-20753	mix	h
dc-20757	res	h
dc-20793	res	m
dc-20807	mix	h
dc-20837	res	l	mid-rise building, use unspecified
dc-20853	com	h
dc-20908	mix	m
dc-20920	mix	h
dc-20921	mix	m
dc-20932	mix	m
dc-20933	mix	h
dc-20974	ind	m	warehousing+office+ltd commercial
dc-21007	mix	h
dc-21050	com	m	health/wellness commercial+ltd residential
dc-21084	ind	h
dc-21088	res	m
dc-21089	ind	m	business employment
dc-21121	ind	m
dc-21128	mix	m
dc-21131	res	h
dc-21135	mix	h
dc-21136	inst	l	child care or small residential
dc-21142	com	h
dc-21145	com	m
dc-21149	res	l	continuing care retirement community
dc-21159	res	h
dc-21176	mix	m
dc-21178	res	h
dc-21179	mix	h
dc-21193	res	m	supportive housing+community services
dc-21205	ind	l	interim low-intensity outdoor uses
dc-21250	res	h
dc-21276	mix	m	mixed use + car dealership
dc-21312	ind	m	business employment
dc-21338	ind	m
dc-21355	com	h
dc-21391	com	l	perinatal health services in garden suite
dc-21393	res	m
dc-21423	com	h
dc-21437	unknown	l	no purpose text
dc-21459	ind	m
dc-21463	mix	h
dc-21464	res	h
dc-21471	mix	m
dc-21483	com	m	historic Strathcona core commercial
dc-21486	mix	m
dc-21522	res	m
dc1-10468	com	l	Telephone Exchange historic, use unspecified
dc1-10705	unknown	l	fragment only
dc1-10886	res	l	single family structure preservation
dc1-11240	res	l	senior's residence (St Joseph's Hospital)
dc1-11400	unknown	l	generic DC district, no use
dc1-11619	unknown	l	no purpose text
dc1-11699	unknown	l	no purpose text
dc1-12034	res	m	Ross Flats Apartment historic
dc1-12157-area-1	unknown	l	fragment only
dc1-12356	res	h
dc1-12482	com	l	HBC Department Store facades
dc1-12800	com	l	Churchill Wire Centre facades
dc1-12801	unknown	l	no purpose text
dc1-12929	com	l	McLeod Building historic office
dc1-13175	unknown	l	no purpose text
dc1-13817	mix	m	Hugh Duncan Residence commercial+residential
dc1-13838	inst	h	Strathcona Library
dc1-14006	res	m	Bard Residence
dc1-14184	com	l	Hagmann Block historic
dc1-14204	res	m
dc1-14446	res	h
dc1-14448	inst	l	Rehwinkel Parsonage historic
dc1-14507	inst	m	Connaught Armoury historic
dc1-14553	res	m	Arlington Apartment historic
dc1-14647	res	m	William Blakey Residence
dc1-14667	com	h	Shopping Centre Zone
dc1-14681	mix	m	George Durrand Residence commercial+residential
dc1-14690	res	h
dc1-14732	res	h
dc1-14928	res	h
dc1-14965	res	h
dc1-15020	res	h
dc1-15056	com	h	Shopping Centre Zone
dc1-15317	res	m	medium/high density residential urban village
dc1-15386	res	m	Ingebert Olson Residence
dc1-15411	inst	l	Immigration Hall historic
dc1-15421	res	m	Foote Residence/Parkview Apartments
dc1-15451	res	h
dc1-15578	mix	l	Hull Block, range of uses+ltd residential
dc1-15751	com	m	Duggan Residence office use
dc1-15767	mix	l	existing residential + allow industrial
dc1-15946	mix	m	commercial+medium-density residential
dc1-15964	res	h	reverse housing
dc1-16022	res	h
dc1-16084	res	h
dc1-16129	res	h
dc1-16179	res	h
dc1-16201	res	h
dc1-16225	res	m
dc1-16254	mix	m	commercial+medium-density residential
dc1-16261	res	m
dc1-16270	res	h
dc1-16281	mix	m	low intensity commercial+residential
dc1-16322	res	m	McLuhan Residence, ltd residential/commercial/cultural
dc1-16343	res	h
dc1-16367	res	h
dc1-16399	res	h
dc1-16445	com	h
dc1-16471	mix	m	medium density residential+ground floor commercial
dc1-16473	res	h
dc1-16535	res	l	Le Marchand historic, use unspecified
dc1-16547	mix	m	Kelly Ramsey block multi-use
dc1-16602	unknown	l	fragment only
dc1-16613	ind	m	business employment
dc1-16693	res	h
dc1-16763	res	m	John T Ross Residence + high density residential
dc1-16784	mix	m	low density mixed use residential+commercial
dc1-16797	res	m	A.K. Buckham Residence
dc1-16894	res	h
dc1-17014	res	m	Hyndman Residence
dc1-17020	res	h
dc1-17028	res	h
dc1-17111	inst	m	Public Utility uses
dc1-17121-shallow-lot-0	res	h
dc1-17121-stacked-row-housing	res	h
dc1-17178	mix	m	high density residential tower+street commercial
dc1-17355	mix	h	mixed use residential+commercial LRT
dc1-17382	inst	m	Public Utility+Commercial+Community Service
dc1-17410	res	h
dc1-17414	res	h
dc1-17470-area-1	res	h
dc1-17470-area-2	res	h
dc1-17485	res	m	Coates Residence
dc1-17646	mix	m	Phyllis Grocery Store historic, commercial+residential
dc1-17690	res	h
dc1-17829	com	l	Gem Theatre facades historic
dc1-17844	unknown	l	no purpose text
dc1-17848	mix	h	high density commercial+residential Whyte Ave
dc1-17874	res	m	Hunt Residence
dc1-17884	res	h
dc1-17918	inst	l	Church Street heritage character
dc1-18049	mix	h	commercial/residential/office/entertainment/cultural/institutional
dc1-18099-area-1	mix	h	retail/office/entertainment/residential
dc1-18099-area-2	mix	h	commercial+residential
dc1-18099-area-5	mix	m	mixed use retaining residential
dc1-18123	mix	l	Boyle Renaissance, use unspecified
dc1-18136	res	h
dc1-18153	res	h
dc1-18175-hecla-block	com	l	Hecla Block historic
dc1-18179	unknown	l	no purpose text
dc1-18190	mix	m	Shop-Easy Grocery historic, commercial+residential
dc1-18203	res	h	reverse housing
dc1-18205	res	h
dc1-18253	res	h
dc1-18332	unknown	l	no purpose text
dc1-18440	res	h
dc1-18448	mix	m	Wallbridge Residence residential+commercial
dc1-18461	mix	m	heritage area, business commercial+residential
dc1-18468	inst	m	extended medical treatment services
dc1-18497	res	h
dc1-18559	com	h
dc1-18583	mix	m	Gibbard Block historic mix of uses
dc1-18591	res	m	Rodd Apartments historic
dc1-18597	com	h	shopping centre
dc1-18607	res	h
dc1-18626	inst	l	Oblats Maison Provinciale historic
dc1-18632	res	h
dc1-18680	res	h
dc1-18685-area	res	h
dc1-18685-area-b	res	h
dc1-18712	res	m	Alex Cormack Residence
dc1-18748	res	h
dc1-18769	res	h
dc1-18795	res	h	reverse housing
dc1-18832	res	m	Griffith Residence
dc1-18836	inst	m	institutional/community service
dc1-18848	mix	m	existing commercial + transit-oriented residential mixed use
dc1-18885	com	m	Street Railway Substation adaptive reuse commercial
dc1-18890	inst	m	solar utility + water treatment + community/cultural
dc1-18922	res	h
dc1-18934	res	m	single-detached historic context
dc1-19022	mix	m	Douglas Manor historic mixed-use
dc1-19035	mix	h	commercial+residential
dc1-19051	mix	m	Stovel Block historic range of uses
dc1-19066	res	h
dc1-19115	inst	m	Ortona Armoury arts/community hub
dc1-19135	mix	m	Rossdale Brewery historic, residential/parks/commercial/cultural
dc1-19186	res	h	reverse housing
dc1-19232	res	h
dc1-19266	res	m
dc1-19270	unknown	l	no purpose text
dc1-19308	res	h
dc1-19316	res	h
dc1-19331	mix	m	Delton Grocery historic commercial+residential
dc1-19382	res	m	medium density residential+ltd commercial
dc1-19431	com	m	Community Commercial Centre
dc1-19477	res	m	Walton L Smith Residence
dc1-19485-area	res	h
dc1-19485-area-b	res	h
dc1-19485-area-c	res	h
dc1-19485-area-d	res	h
dc1-19505	inst	h	Hospital and Health Campus
dc1-19506	inst	m	Friary/College heritage institutional
dc1-19509	res	h
dc1-19546	res	h
dc1-19568	res	h
dc1-19570	res	h
dc1-19628	inst	m	Aviation Museum historic
dc1-19636	res	h
dc1-19662	com	m	Telephone Exchange historic + new commercial
dc1-19663	res	m	RLD lot wellsite
dc1-19674	res	h
dc1-19693	res	h
dc1-19714	res	m	mid-rise residential + CPR Station preservation
dc1-19719	unknown	l	no purpose text
dc1-19743-area	res	h
dc1-19743-area-b	res	h
dc1-19755	com	m	Ritchie Mill historic commercial
dc1-19761	com	h
dc1-19771	inst	m	LRT Station + park and ride
dc1-19789	res	m	Cecil Burgess Residence + garden suite
dc1-19798	ind	m	business employment mix commercial/business/light industrial
dc1-19816	unknown	l	no purpose text
dc1-19827	res	h
dc1-19835	mix	m	commercial+institutional+residential
dc1-19847	mix	m	residential+commercial Desrochers LRT
dc1-19860	mix	m	mixed use high rise + historic facades
dc1-19863	mix	m	John L Lang Apartments historic commercial+residential
dc1-19884	com	h	commercial shopping centre
dc1-19887	res	h
dc1-19888	mix	m	Barto Residence historic residential+non-residential
dc1-19932	res	h
dc1-19966	res	h
dc1-19988	mix	m	historic 81 Ave commercial+mixed use
dc1-19998	res	h
dc1-20060	res	h
dc1-20093	res	h
dc1-20124-area	res	h
dc1-20124-area-b	res	h
dc1-20164-area-5	unknown	l	no purpose text
dc1-20167	res	m	Magrath Mansion historic
dc1-20181	mix	m	Hangar 11 historic adaptive reuse mixed-use
dc1-20229	res	h
dc1-20285	res	h
dc1-20301	res	m	mixed-use predominantly residential
dc1-20340	com	m	Community Commercial Centre
dc1-20354	res	h
dc1-20433	mix	m	mixed use high density
dc1-20460	inst	m	Loyal Orange Lodge community/cultural
dc1-20462	mix	m	mixed use commercial/residential/office
dc1-20477	mix	m	Transit Hotel urban village
dc1-20518	mix	m	high density mixed-use urban village
dc1-20538	mix	m	Balfour Manor historic mix of uses
dc1-20649	res	h
dc1-20650	res	h
dc1-20651	res	h
dc1-20692	ind	m	business industrial + commercial
dc1-20696	res	m	single family/low-rise/medium mix + local uses
dc1-6220	unknown	l	no purpose text
dc1-6380	unknown	l	no purpose text
dc1-6502	unknown	l	generic DC district, no use
dc1-7085	res	h	multiple family/row housing
dc1-9508	ind	m	industrial and commercial business
dc2-100	res	m	day care + row housing
dc2-1002	res	h
dc2-1006	mix	m	mixed-use mid-rise
dc2-1007	res	h
dc2-1008	res	h
dc2-1009	mix	m	residential+commercial+ltd community
dc2-101	com	m	neighbourhood convenience commercial+club
dc2-1010	com	h	shopping center
dc2-1014	com	h
dc2-1015	com	l	interim commercial/institutional/recreational
dc2-1018	com	m	convenience commercial+personal service
"""
_P2 = """
dc2-1019	com	m	commercial+office+ltd residential
dc2-102	com	m	general business
dc2-1020	res	h	high-rise residential tower
dc2-1024	com	m	neighbourhood convenience commercial
dc2-1025	mix	m	two high rise residential + commercial podium
dc2-1027	res	m	high-rise apartment + ground commercial
dc2-1028	ind	m	industrial business + offices + ltd commercial
dc2-1030	ind	m	non-industrial businesses + retail supplement to industrial
dc2-1031	res	h	high-rise residential
dc2-1032	res	m	12-bedroom Group Home
dc2-1035	com	m	retail-business + highway commercial
dc2-1036	mix	m	vehicle-oriented commercial+medium rise residential
dc2-1037	res	h	high-rise apartment
dc2-1038	com	h	neighbourhood commercial
dc2-1039	mix	m	high density residential tower + mix of uses
dc2-1040	com	m	convenience commercial+personal service
dc2-1041	com	m	convenience commercial+personal service
dc2-1042	res	h	low rise residential
dc2-1045	res	h	Single Detached House
dc2-1046	com	m	small-scale commercial/retail/office
dc2-1047	com	m	retail/office/business
dc2-1048	com	m	highway commercial+retail+industrial business
dc2-1049	ind	l	private education + future industrial businesses
dc2-1050	mix	m	medium density mixed use
dc2-1051	inst	m	seniors residence+extended medical+institutional
dc2-1053	res	h	Row Housing
dc2-1054	res	h	high density residential
dc2-1055	res	h	Row Housing infill
dc2-1056	inst	m	Derrick Golf and Winter Club recreation
dc2-1057	res	m	low intensity residential
dc2-1058	mix	m	Bonnie Doon town centre mixed-use
dc2-1059	mix	m	mixed use commercial/residential
dc2-106	com	m	convenience commercial+personal service
dc2-1060	mix	m	arts/entertainment/education/ltd residential/district energy
dc2-1061	com	h	vehicle-oriented commercial
dc2-1062	ind	m	general industrial + conversion to commercial office
dc2-1063	com	l	single detached or small health services
dc2-1064	res	m	two high rise residential + non-residential podium
dc2-1066	com	m	retail/general commercial/office
dc2-1067	res	m	two high rise residential + complementary podium
dc2-1068	mix	m	two residential towers + street commercial
dc2-1069	mix	m	podium+tower ground-oriented commercial
dc2-107	res	h	single detached dwellings
dc2-1070	ind	m	mixed commercial and industrial
dc2-1074	ind	h	Edmonton Waste Management Centre
dc2-1075	com	m	general commercial + low intensity office
dc2-1076	com	m	range of commercial amenities
dc2-1078	ind	m	industrial + limited commercial
dc2-1079	com	m	commercial development
dc2-1081	mix	m	existing mixed-use building Jasper Ave
dc2-1082	mix	m	Hotel Macdonald mixed use residential+commercial
dc2-1083	mix	m	mixed use high rise
dc2-1084	mix	m	commercial + medium density residential
dc2-1085	inst	l	religious assembly + medium-density residential
dc2-1086	com	h	medium intensity commercial office
dc2-1087	com	m	low intensity commercial office/retail/service
dc2-1090	mix	m	mixed use podium+tower Jasper Ave
dc2-1092	res	m	seniors-oriented low rise apartments
dc2-1095	res	h	residential on surplus school site
dc2-1096	com	m	general business+commercial+ltd business industrial
dc2-1097	res	h	single detached residential
dc2-11	com	m	Site Specific Commercial District
dc2-1100	mix	m	mixed use node LRT + ground floor commercial
dc2-1102	ind	m	General Industrial + Commercial
dc2-1103	res	h	Multi-unit Housing shallow lots
dc2-1104	mix	m	small scale commercial + residential
dc2-1105	res	h	Row Housing
dc2-1106	mix	m	single detached + commercial component
dc2-1107	com	h	highway/general commercial
dc2-1108	com	h	highway/general commercial
dc2-1110	com	h	highway/general commercial
dc2-1112	com	h	highway/general commercial
dc2-1113	com	m	commercial/light industrial/automotive/service
dc2-1114	com	l	temporary event parking
dc2-1116	res	m	mixed-use primarily residential + ltd commercial
dc2-1118	com	m	range of commercial
dc2-1119	mix	m	commercial + medium density residential
dc2-112	com	m	industrial business+commercial, auto dealership
dc2-1120	res	h	multi-residential tiny home community
dc2-1121	res	h	multi-unit mid-rise
dc2-1122	res	m	low-rise residential + neighbourhood commercial
dc2-1123	res	h	Row Housing
dc2-1125	mix	m	Multi-Unit + ground floor commercial
dc2-1127	res	h	mid rise high density residential
dc2-1128	com	m	low-intensity commercial
dc2-1129	com	m	low-intensity commercial
dc2-113	com	m	gas bar + convenience commercial
dc2-1130	com	m	convenience commercial + business
dc2-1131	inst	m	religious assembly + private education
dc2-1132	com	m	variety of commercial
dc2-1136	com	m	neighborhood convenience + personal service
dc2-1137	res	h	large lot single detached
dc2-1138	res	m	Charles Camsell Hospital redevelop to Multi-unit Housing
dc2-1139	com	m	non-residential Calgary Trail corridor
dc2-1140	com	m	low-intensity non-residential
dc2-1142	res	m	mid-rise residential + ltd neighbourhood commercial
dc2-1143	com	m	retail + ltd general commercial
dc2-1145	com	m	convenience commercial
dc2-1146	com	h	shopping centre
dc2-1147	res	h	Single Detached Multi-unit Project
dc2-1148	com	m	convenience commercial
dc2-1149	com	m	convenience commercial + future redevelopment
dc2-115	com	m	low intensity commercial/office/service
dc2-1150-area-a	com	m	community commercial
dc2-1150-area-b	com	m	community commercial
dc2-1151	inst	m	publicly owned health care facility
dc2-1152	res	h	mid-rise apartment
dc2-1154	res	h	mid-rise residential
dc2-1155-area-a	com	m	retail/general commercial/office
dc2-1155-area-b	com	m	retail/general commercial/office
dc2-1158	res	h	residential attached dwellings
dc2-1159	res	m	small scale residential + ltd commercial
dc2-116	res	h	medium density single storey residential
dc2-1160	res	h	residential high-rise
dc2-1161	res	h	Multi-unit row housing
dc2-1164	res	h	Multi Unit Row Housing
dc2-1165	mix	m	shopping centre commercial + medium density residential
dc2-1166	res	h	medium-rise residential
dc2-1167	res	h	multi-unit residential
dc2-1168	com	m	range of commercial
dc2-1169	mix	m	six storey mixed use residential+commercial
dc2-1171	mix	m	medical+commercial+residential node
dc2-1174	res	h	small lot Single Detached
dc2-1176	mix	m	low rise Multi-unit + institutional + commercial
dc2-1177	mix	m	mixed-use commercial+residential
dc2-118	com	m	low intensity commercial
dc2-1179	res	h	low-rise residential
dc2-1180	mix	m	residential/commercial mixed-use options
dc2-1181	res	h	low-medium density residential
dc2-1182	com	m	community level commercial
dc2-1184	res	m	mid-rise residential + ltd commercial
dc2-1185	res	h	high rise residential
dc2-1186	res	m	Clifton Place mixed use primarily residential
dc2-1188	mix	m	mid-rise residential w/ commercial + low rise commercial
dc2-1189	com	m	retail commercial + office
dc2-1190	com	h	large general retail store
dc2-1191	com	h	highway/general commercial
dc2-1192	com	h	highway/general commercial
dc2-1194	res	h	two row housing buildings
dc2-1195	unknown	l	no purpose text
dc2-1196	res	h	low rise Multi-unit Housing
dc2-1198	mix	m	West Edmonton Mall diverse uses
dc2-12	com	m	commercial development
dc2-1200	com	m	commercial + extended medical treatment
dc2-1201	com	m	commercial serving community
dc2-1202	res	h	ground oriented Multi-unit Row Housing
dc2-1204	ind	m	industrial businesses + ltd non-industrial
dc2-1205	res	h	Multi-unit Row Housing
dc2-1206	res	h	single detached residential
dc2-1207	mix	m	commercial + mixed-use residential option
dc2-1208	com	h	auto-oriented + shopping centre
dc2-1209	mix	m	high rise + ground dwellings + street commercial
dc2-1210	ind	m	industrial businesses + ltd non-industrial
dc2-1211	com	m	low intensity commercial/office/service + ltd residential-related
dc2-1212	res	h	Multi-unit row housing
dc2-1213	com	m	medical office+treatment facility+commercial
dc2-1215	res	h	small scale housing
dc2-1216	res	h	small scale housing
dc2-1217	res	h	6-storey multi-family residential
dc2-1218	mix	m	education/commercial/office/light industrial
dc2-1219	res	m	medium density residential + small commercial
dc2-122	inst	m	religious assembly + related uses
dc2-1220	mix	m	residential Multi-unit + main floor commercial + standalone commercial
dc2-1222	res	h	low/medium rise Multi-unit
dc2-1223	res	h	Single Detached/Semi/Duplex Multi-unit Project
dc2-1224	res	h	Single/Semi/Duplex
dc2-1226	mix	m	multi-unit housing + standalone commercial
dc2-1227	com	m	low intensity commercial/office/service
dc2-1229	res	m	high density residential apartment
dc2-123	com	m	convenience commercial + ltd general business
dc2-1230	res	m	medium-rise high density residential + ltd commercial
dc2-1231	res	h	Multi-unit Row Housing
dc2-1232	res	h	medium-rise ground-oriented units
dc2-1233	inst	m	seniors: residential/institutional/assisted living/medical
dc2-1234	ind	m	industrial businesses + Public Education
dc2-1235	res	h	small scale infill housing
dc2-1236	res	h	mid-rise residential
dc2-1237	inst	m	live theatre/cultural/railway exhibit Bus Barns
dc2-1238	res	h	medium density Multi-Unit
dc2-1240	com	m	commercial shopping centre + self-storage/office/entertainment
dc2-1241	mix	m	high density mixed-use commercial + high rise residential
dc2-1242	res	m	residential + ltd non-residential ground
dc2-1243	mix	m	commercial/office/health/community/recreational/educational
dc2-1244	res	h	medium density Multi-Unit
dc2-1245	ind	m	industrial businesses + Public Education
dc2-1247	ind	m	veterinary hospital + apt hotels + medium industrial
dc2-1248	com	m	low intensity commercial/office/service
dc2-128	com	l	Non-accessory Parking additional to RA7
dc2-129	mix	m	high rise residential/commercial
dc2-132	com	m	ltd commercial serving local residents
dc2-133	com	m	convenience commercial + ltd general business
dc2-135	com	m	convenience commercial + personal service
dc2-136	com	m	convenience commercial + personal service
dc2-14	res	h	multiple family housing + apartments
dc2-140	com	h	grocery/drug store + highway commercial
dc2-142	inst	m	Bissell Centre outreach ministry social service
dc2-144	inst	m	low intensity institutional + professional office
dc2-147	inst	l	religious assembly + seniors apartment
dc2-148	res	h	low-medium density residential row housing
dc2-150	com	m	gas bar + convenience store
dc2-151	res	h	low-medium density residential single/semi/row
dc2-154	res	h	semi-detached + single family housing
dc2-162	inst	m	religious assembly + private education
dc2-163	com	m	general business-office
dc2-165	com	m	highway commercial
dc2-166	com	m	parkade for automotive dealership
dc2-170	inst	l	day care support business + RF3 residential
dc2-171	com	m	automotive repair facility
dc2-173	inst	h	156 bed nursing home
dc2-175	res	h	low-medium density residential semi/row
dc2-176	mix	m	single detached conversion to offices/retail
dc2-177	ind	m	truck/mobile home sales + flea market + industrial business
dc2-17a	res	h	semi-detached/duplex/row housing
dc2-17b	res	h	medium rise apartment
dc2-180	ind	m	mixed industrial business + hotel
dc2-181	com	m	specified commercial + general business
dc2-183	com	m	convenience commercial + personal service
dc2-184-area-2	res	h	low-medium density residential semi/row
dc2-186	res	h	16 town homes
dc2-188	com	m	low intensity retail/commercial/office/service
dc2-189	com	m	retail/general commercial/office
dc2-19	com	h	shopping centre
dc2-190	com	m	general business + personal service
dc2-196	com	m	convenience commercial/personal service/religious assembly
dc2-197	mix	m	single detached conversion to retail/personal service
dc2-198	res	h	low-medium density residential semi/row
dc2-20	mix	m	high rise apartment + variety commercial
dc2-204	res	h	semi-detached + single family
dc2-205	com	m	retail business + highway commercial
dc2-206	res	h	low-medium density multiple family semi/row/stacked
dc2-21	res	h	multiple family housing row/stacked/apartments
dc2-212	res	h	low-medium density residential row housing
dc2-214	res	m	low rise apartment + church parking
dc2-216	inst	m	Urban Services + Youth Emergency Shelter
dc2-217	mix	m	speciality retail/personal service + single detached
dc2-218	res	h	low-medium density residential semi/row
dc2-221	inst	l	accessory parking for religious assembly/education
dc2-223	res	l	child care centre + row housing
dc2-224	res	h	Townhouses/Row/High Rise Apartment
dc2-226	mix	m	seniors apartment + main floor offices/services
dc2-229	res	m	high rise apartment + ltd ancillary
dc2-230-area	com	m	convenience commercial + personal service
dc2-230-area-b	res	h	low-medium density residential semi/row
dc2-231	res	h	medium density residential semi/row
dc2-232	com	m	small retail + general commercial
dc2-234	inst	h	religious assembly
dc2-236	res	h	semi-detached housing
dc2-238	res	h	medium rise apartment
dc2-240	com	m	small retail + general commercial
dc2-241	com	m	convenience commercial + personal service
dc2-242	mix	m	medium density multiple family + office conversion
dc2-244	res	m	high rise apartment + ltd ancillary
dc2-250	com	l	medium intensity office + conversion to religious assembly
dc2-256-area-1	com	l	surface parking for Ritchie Mill/park
dc2-256-area-2	com	l	public parking Bus Barns
dc2-256-area-3	inst	l	Bus Barns marketing + cultural uses
dc2-259	com	m	convenience commercial + personal service
dc2-261	res	m	ltd residential + religious assembly transition
dc2-263	mix	m	apartment/stacked/linked + ltd commercial
dc2-269	ind	m	industrial business + spectator entertainment
dc2-270	com	m	ltd commercial CSC
dc2-272	ind	h	waste management facility
dc2-273	res	m	low rise apartment + health services
dc2-277	res	m	low-medium density residential semi/row + religious assembly
dc2-279	res	m	low rise apartment + health services
dc2-28	com	m	Site Specific Commercial Calgary Trail
dc2-281	com	m	commercial+office+ltd residential
dc2-283-area-b	res	h	hi-rise residential
dc2-284	res	h	Low Rise Apartment
dc2-287	res	h	low rise apartment
dc2-288	res	h	low-medium density residential row housing
dc2-289	com	m	medical office park + ltd commercial + shelter
dc2-290	res	m	ltd residential + related uses
dc2-291	com	m	small retail + general commercial
dc2-292	inst	m	Edmonton Police district station
dc2-293	res	m	ltd residential + related
dc2-295	com	m	funeral + cremation/interment services
dc2-299	com	m	convenience commercial + automotive service
dc2-305-area-c	res	h	low-medium density multiple family
dc2-306	res	h	medium density residential row + low rise apartments
dc2-309	com	m	broad range commercial and office
dc2-31	res	h	four dwelling units existing building
dc2-310	inst	m	EMS ambulance station
dc2-312-area	res	h	low density multiple family residential
dc2-312-area-b	com	m	convenience commercial/personal service/religious assembly
dc2-315-area-b-east-side	res	h	low-medium density residential semi/row
dc2-315-area-west-side	res	h	medium density residential semi/row
dc2-316	ind	m	industrial business + Animal Hospital/Shelter
dc2-319	com	m	commercial + automotive dealership
dc2-320	mix	m	low density residential + neighbourhood commercial
dc2-323	res	m	ltd residential + related
dc2-324	com	m	retail commercial/amusement/office
dc2-325	com	m	businesses large sites 118 Avenue
dc2-326	com	m	neighbourhood convenience commercial + auto sales
dc2-327	res	h	low rise walkup apartment
dc2-328	res	h	medium rise apartment
dc2-329	res	h	Medium Density Stacked Townhouse
dc2-332	com	m	retail + highway commercial
dc2-334	inst	l	existing building commercial/community/educational/recreational/cultural
dc2-335	com	m	general business large site
dc2-336	res	h	low-medium density residential semi/row
dc2-338	res	h	low-medium density residential semi/row
dc2-339	res	h	low-medium density residential semi/row
dc2-340	com	m	retail commercial/amusement/office
dc2-342	inst	m	prison for Federally Sentenced Women
dc2-343	com	m	retail business + highway commercial
dc2-345	com	m	office building + highway commercial
dc2-348	com	m	funeral + cremation/interment services
dc2-349	res	h	low rise apartment
dc2-350	inst	m	Tourist Campsite + banquet
dc2-351	com	m	retail/general commercial/office
dc2-36	mix	l	interim convenience commercial then residential RA7
dc2-360	inst	m	EMS ambulance station
dc2-364	inst	m	religious assembly + bookstore/ministry/educational
dc2-367	inst	m	community service + ltd low intensity commercial
dc2-369	res	h	rural residential
dc2-370	res	m	low density single detached
dc2-371	res	m	low density single detached
dc2-372	res	m	low density single detached
dc2-373	res	m	low density single detached
dc2-376	res	h	family-oriented housing three units
dc2-378	res	h	up to four dwellings
dc2-379	res	h	medium density multiple family
dc2-380	res	h	medium density multiple family semi/duplex/row
dc2-384	com	m	general business + retail
dc2-385	res	m	medium density residential Mill Creek Ravine
dc2-386	res	m	low density multiple family
dc2-393	inst	m	institutional/community service facilities
dc2-394	com	m	neighbourhood convenience + highway commercial
dc2-396	com	m	vehicle orientated commercial
dc2-399	com	m	general business + vehicle body repair
dc2-400	res	h	Suburban Estate Lots
dc2-401	com	m	convenience commercial/personal service/minor alcohol
dc2-403	res	m	medium density residential Garneau
dc2-404	ind	m	industrial business no nuisance
dc2-406	com	m	ltd commercial
dc2-410	res	m	seniors medium density row housing
dc2-412	res	m	Medium Density Multiple Family + ancillary services
dc2-413	com	m	conversion of apartment to commercial
dc2-415	res	h	low rise apartment
dc2-418	ind	m	medium industrial
dc2-420	com	m	general business 100 Avenue
dc2-421	ind	m	warehousing to service retail
dc2-422	inst	m	private/public recreation/institutional/community
dc2-423	com	l	Non-accessory Parking additional to RA7
dc2-426	com	l	accessory surface parking Professional Centre
dc2-427	res	h	mixed housing semi/row/low rise apartments
dc2-429	com	m	variety commercial large site
dc2-43	com	m	general business
dc2-432	res	h	single family residential
dc2-433	com	l	landscaped parking for commercial site
dc2-435	ind	m	Industrial/Business + Casinos
dc2-436	mix	m	retail + office + medium rise residential
dc2-437	com	m	highway commercial + ltd industrial
dc2-439	res	h	single detached residential
dc2-440	res	h	low-medium density residential semi/row
dc2-445	res	m	adult-oriented residential + religious assembly
dc2-448	res	h	medium density semi/row
dc2-449	com	m	general business employment
dc2-452	com	m	large shopping centre + mixed uses
dc2-455	com	m	convenience commercial
dc2-457	com	m	low intensity commercial office/retail/service
dc2-458	ind	m	commercial + industrial business area
dc2-46	com	m	truck/automotive/recreational vehicle sales
dc2-460	res	m	Medium Density Multiple Family + ancillary services
dc2-462	inst	m	EMS ambulance station
dc2-463	com	m	entertainment centre hotel/casino/theatre
dc2-466	com	m	general commercial + low intensity office
dc2-467	mix	m	office conversion to apartment + commercial/office
dc2-468	com	m	professional office + single apartment unit
dc2-470	com	m	convenience commercial
dc2-472	mix	m	mixed housing row/apartment + ltd commercial Downtown
dc2-474	com	m	convenience commercial + personal service
dc2-475	ind	m	industrial businesses no nuisance
dc2-478	com	m	convenience commercial + personal service
dc2-483	ind	m	industrial businesses no nuisance
dc2-484	res	h	low density multiple family semi/row
dc2-485	com	m	large shopping centre + mixed uses
dc2-486	com	m	hotel
dc2-489	com	m	neighbourhood convenience commercial + personal service
dc2-490	com	m	range of commercial
dc2-491	com	m	range of commercial
dc2-497	res	m	medium density residential + related
dc2-501	mix	m	commercial+residential+community+office Downtown
dc2-505	mix	m	medium density residential + commercial + open space Oliver
dc2-511	ind	m	Casinos + industrial businesses
dc2-515	com	m	wide range commercial large site
dc2-516	ind	m	medium industrial + private clubs/recreation/cultural
dc2-520	ind	m	industrial businesses no nuisance
dc2-522	inst	h	auxiliary hospital
dc2-523	com	m	regional level commercial
dc2-524	inst	m	oil field equipment museum + private club
dc2-527	inst	l	religious assembly + seniors housing
dc2-529	inst	m	seniors housing + extended care lodge + commercial
dc2-530	res	m	medium density residential + related
dc2-531	res	m	medium density residential + assisted living
dc2-533	com	m	convenience commercial/gas bar/car wash
dc2-535	com	m	greenhouse/nursery/retail store
dc2-536	res	m	non-family medium density residential
dc2-537	ind	m	Casinos + IB Industrial Business
dc2-54	inst	h	200-bed auxiliary hospital
dc2-544	mix	m	extended medical + medium density housing + ltd commercial
dc2-545	res	m	medium density housing
dc2-546	res	h	single and semi-detached residential
dc2-547	com	m	convenience commercial + personal service + minor alcohol
dc2-550	res	h	single family residential rural
dc2-551	com	m	convenience commercial + personal service
dc2-552	com	m	convenience commercial + personal service + clinic
dc2-553	com	m	ltd commercial
dc2-554	mix	m	office support service + semi-detached housing
dc2-555	res	h	family oriented dwellings semi/duplex/row
"""
_P3 = """
dc2-556	res	h	low density residential
dc2-557	mix	m	ground floor commercial to apartment + small commercial
dc2-559	com	m	small scale retail + general commercial
dc2-560	res	h	low rise apartment housing
dc2-561	com	m	large scale retail business + general commercial
dc2-562	com	m	businesses large sites visibility
dc2-563	res	m	low rise apartment
dc2-566	res	m	medium density residential + related
dc2-567	com	m	commercial/business + general retail
dc2-569	res	m	low and medium density housing
dc2-573	com	m	automobile oriented commercial
dc2-574	ind	m	industrial businesses + medium industrial manufacturing
dc2-575	com	m	call centre + office support + commercial schools
dc2-577	res	h	medium-high density Row/Stacked/High Rise Apartment
dc2-583	ind	m	general industrial + ltd industrial business
dc2-589	res	h	low density residential semi-detached
dc2-591	res	m	seniors residential + convenience commercial
dc2-593	com	m	Automotive/Recreational Vehicle Sales
dc2-594	inst	m	assisted living seniors geriatric/palliative care
dc2-596	res	h	Medium Rise Apartment
dc2-602	res	h	Low Rise Apartment
dc2-603	com	m	coffee shop drive-through
dc2-604	inst	l	surface parking for religious assembly
dc2-607	res	h	apartment housing
dc2-608	res	h	apartment housing
dc2-609	com	m	general business + office 100 Avenue
dc2-61	com	m	low intensity business + commercial
dc2-612	com	m	Automotive/Recreation Vehicle Sales
dc2-614	res	h	low and medium density housing
dc2-615	res	h	medium density residential low rise apartment
dc2-616	res	h	low-rise low density apartment
dc2-618	res	m	church parking + residential row housing
dc2-619	com	m	Recycling Depot + small scale commercial
dc2-620	res	h	four-storey low rise residential
dc2-626	com	m	Automotive/Recreational Vehicle Sales
dc2-631	res	h	low and medium rise residential apartment
dc2-632	com	m	existing shopping centre + new commercial
dc2-633	mix	m	mixed use commercial/residential
dc2-635	com	l	surface parking Northlands Park expansion
dc2-636	inst	m	seniors health service facility + parkade
dc2-637	com	m	funeral/cremation/internment facility
dc2-63a	com	m	general business + highway commercial
dc2-641	com	m	retail/commercial/office/indoor storage
dc2-643	com	m	shopping centre
dc2-644	com	m	Casino facility expansion
dc2-645	com	m	office building Professional/Financial/Office Support
dc2-648	mix	m	low intensity business + apartment housing
dc2-650	inst	m	religious assembly
dc2-654	com	m	commercial + industrial business uses
dc2-655	com	m	general retail stores
dc2-66	com	m	general business
dc2-660	inst	m	Traditional Burial Grounds/Cemetery + park
dc2-661	com	m	retail + ltd general commercial Mill Woods
dc2-663	res	m	residential development
dc2-664	res	h	low rise apartment housing
dc2-666	res	h	low rise apartment building
dc2-668	com	m	prestige office buildings + business support/commercial
dc2-67	inst	m	Private Educational/Community Recreational/Private Clubs
dc2-671	ind	m	general industrial + conversion to commercial office
dc2-673	com	m	parking garage for hospital + auto sales
dc2-675	inst	m	La Cite Francophone cultural centre
dc2-676	inst	h	public school
dc2-68	com	m	convenience commercial + office
dc2-684	inst	m	extended medical + seniors + institutional Griesbach
dc2-686	com	m	medium rise office building + commercial
dc2-687	com	m	Southgate Centre shopping centre
dc2-688	res	m	medium density residential Athlone
dc2-689	res	h	medium density residential apartment
dc2-695	ind	m	conversion of obsolete industrial to commercial office
dc2-696	ind	m	general industrial + conversion to commercial office
dc2-697	com	m	office/convenience commercial/library/cultural
dc2-698	res	h	low density housing Griesbach
dc2-699	inst	m	Outdoor/Indoor Participant Recreation + riding stable
dc2-7	com	l	parking lot to serve commercial site
dc2-70	com	m	drive-through vehicle service + convenience commercial
dc2-700	ind	m	general industrial + warehouse sales + restaurant
dc2-704	res	m	low rise apartment + community recreation
dc2-717	inst	m	cemetery + funeral/cremation/internment
dc2-718	res	h	four storey low rise apartment
dc2-719	mix	m	16 storey residential tower + office/commercial podium
dc2-720	res	h	medium density residential apartment
dc2-721	res	m	conversion to apartment housing
dc2-724	res	m	high density residential urban village
dc2-725	res	h	Apartment Housing
dc2-726	res	h	Row Housing
dc2-727	inst	m	public land recreation/stormwater/natural area
dc2-728	res	h	26 storey residential apartment
dc2-732	mix	m	high density mixed use commercial+residential 82 Ave
dc2-736	res	h	row housing
dc2-738	com	m	low intensity neighbourhood convenience commercial
dc2-740	res	h	low rise apartment
dc2-745	res	h	medium rise apartment 6 storeys
dc2-747	mix	m	single detached or professional/office support
dc2-75	com	m	general business + highway commercial
dc2-750	res	m	29 storey high-rise apartment
dc2-751	inst	l	religious assembly + future industrial
dc2-754	inst	m	Regional Health Services Campus
dc2-756	res	h	low rise residential stacked row + apartments
dc2-757	res	h	low rise apartment
dc2-761	res	h	medium density apartment
dc2-768	mix	m	four storey apartment + ground floor commercial
dc2-769	inst	m	seniors Assisted Living + supportive commercial
dc2-771	com	m	commercial hair care in single detached house
dc2-773	com	m	medium rise office building + commercial
dc2-774	res	h	high density residential tower
dc2-775	res	h	four storey low-rise high density apartment
dc2-778	res	h	low-rise apartment affordable housing
dc2-78	inst	m	religious assembly development
dc2-780	mix	m	mixed-use residential + main floor commercial + office
dc2-789	com	m	ltd commercial serving community
dc2-791	com	m	commercial site
dc2-793	com	m	Automotive/Recreational Vehicle Sales
dc2-794	res	h	four storey apartment
dc2-795	res	m	low-rise apartment + child care
dc2-796	mix	m	11-storey mixed-use commercial podium + residential towers
dc2-798	inst	h	nursing home
dc2-799	res	m	apartment housing + extended medical treatment
dc2-800	ind	m	light industrial no nuisance
dc2-801	res	h	row housing
dc2-806	mix	m	residential dwelling + business/office/personal service + studio
dc2-808	com	m	convenience commercial/office/personal services/food
dc2-810	res	m	ground floor commercial in high rise residential
dc2-813	res	h	low-rise residential four storey
dc2-814	res	h	medium density housing
dc2-816	res	h	medium density residential former police station
dc2-817	res	h	multi-unit housing
dc2-820	mix	m	mixed-use high density urban village brownfield
dc2-821	com	m	commercial office within single-detached dwelling
dc2-823	ind	m	general industrial + conversion to commercial office
dc2-824	res	h	high density residential tower
dc2-825	mix	m	36 storey mixed use commercial + high density
dc2-827	res	h	medium density housing
dc2-828	res	h	medium density housing
dc2-829	ind	m	industrial businesses no nuisance + ltd non-industrial
dc2-831	com	m	Automotive/Recreational Vehicle Sales
dc2-836	com	m	convenience commercial + personal service
dc2-837	inst	m	cultural centre
dc2-839	mix	m	36 storey mixed use commercial podium + high density
dc2-842	res	m	two residential dwellings + non-accessory parking
"""
_P4 = """
dc1-12157-area-2	unknown	l	no purpose text
dc2-844	com	m	existing building commercial
dc2-845	com	m	community-oriented commercial business
dc2-847	res	h	Stacked Row Housing
dc2-85	com	m	neighbourhood convenience commercial + personal service
dc2-850	res	h	low rise Apartment Housing
dc2-851	res	m	residential facility for patients/families
dc2-852	mix	m	existing building residential + mixed-use potential
dc2-855	res	m	Group Home
dc2-859	mix	m	Residential above ltd Commercial
dc2-862	com	m	commercial + business near heavy industrial
dc2-863	mix	m	4-storey mixed use residential + commercial
dc2-865	com	m	conversion of residential to health services/office
dc2-867	com	m	three mixed retail/office buildings
dc2-869	mix	m	mixed use residential + commercial Water's Edge
dc2-87	com	m	office/commercial + basic services/community/cultural
dc2-873	res	h	low rise residential
dc2-875	mix	m	mixed use commercial + residential shopping street
dc2-877	res	h	Apartment Housing Family Oriented
dc2-879	com	m	highway commercial 100 Avenue
dc2-88	mix	m	existing hotel + residential related Downtown
dc2-880	res	h	existing residential Griesbach
dc2-888	res	h	semi-detached Housing
dc2-891	res	h	two low rise apartment buildings
dc2-893	com	m	shopping centre anchored by grocery
dc2-896	com	m	vehicle-oriented + general commercial remediated
dc2-898	ind	m	industrial businesses no nuisance + ltd non-industrial
dc2-899	com	m	South Edmonton Common shopping centre
dc2-903	res	m	Stacked Row Housing + religious assembly + community
dc2-907	mix	m	residential + mixed-use residential/commercial
dc2-908	com	m	services and retail serving local area
dc2-909	ind	m	light industrial + ltd retail no nuisance
dc2-911	inst	m	Indoor Participant Recreation rifle/pistol ranges
dc2-918	com	m	three hotels
dc2-921	res	h	medium density housing
dc2-922	res	h	low rise residential
dc2-926	res	m	residential facility for patients/families
dc2-928	mix	m	mixed-use high-rise residential/retail/office
dc2-929	res	h	residential development + natural area
dc2-93	com	m	ltd retail office/business
dc2-930	res	h	high density apartment building
dc2-931	res	h	high density residential building
dc2-934	res	m	low rise residential + Live-Work Units
dc2-938	com	m	Automotive/Recreation Vehicle Sales + repair
dc2-939	res	h	up to four residential units
dc2-941	res	h	semi-detached + row housing
dc2-943	ind	m	industrial businesses no nuisance + ltd non-industrial
dc2-947	res	h	medium density residential Row Housing
dc2-948	mix	m	mixed use high rise + complementary commercial Jasper
dc2-95	com	m	office building health services + ancillary commercial
dc2-950	com	m	ltd low intensity commercial + low impact industrial
dc2-951	com	m	commercial development
dc2-952	mix	m	commercial node + residential/commercial TOD
dc2-957	ind	m	existing religious assembly then manufacturing/industrial
dc2-958	res	m	private park + high rise residential + supportive living
dc2-960	res	m	low rise development shared communal space
dc2-961	com	m	health services/office in single-detached dwelling
dc2-967	res	m	mid rise residential + ltd commercial
dc2-968	ind	m	general industrial + automotive/recreation vehicle sales
dc2-970	res	m	low and mid rise residential + ltd supporting
dc2-971	com	m	low intensity commercial/office/service + lodging houses
dc2-974	res	h	Zero Lot Line Single Detached
dc2-975	mix	m	single detached + small office/commercial + small housing
dc2-976	mix	m	22 storey mixed-use + private education podium
dc2-978	mix	m	low-medium density housing + adaptive reuse + office
dc2-979	com	m	office and commercial development gateway
dc2-98	inst	m	Visitor Information Services Centre + interpretive
dc2-980	com	m	shopping centre + office/entertainment/cultural/education
dc2-983	mix	m	high density residential + hotel transit centre
dc2-984	res	h	Row Housing
dc2-985	ind	m	light industrial + ltd commercial supportive
dc2-987	mix	m	high density residential + street level commercial/community
dc2-988	res	h	low rise high density residential
dc2-989	com	m	highway commercial + automotive/recreational sales
dc2-990	com	m	commercial and business 97 St/Yellowhead
dc2-991	res	h	two six storey apartment buildings
dc2-995	com	m	small scale neighbourhood commercial
dc2-998	mix	m	mixed-use commercial ground floor + residential above
dc2-999	mix	m	mixed-use commercial ground floor + residential above
dc2-b-coast-terrace-plaza	com	l	slug-derived (plaza), no purpose text
dc2-highland-court-agreement-c86	unknown	l	agreement boilerplate, slug ambiguous
dc2-i-plaza-124-agreements	com	l	slug-derived (plaza), no purpose text
dc2-j-united-management-office-building-agreement-c90	com	l	slug-derived (office-building), boilerplate
dc2-k-st-andrews-seniors-centre-agreement-m37	inst	l	slug-derived (seniors-centre), no purpose text
dc2-l-huntington-hill-agreement-m60a	unknown	l	agreement boilerplate, slug ambiguous
dc2-m-maclachlan-mitchell-homes	res	l	slug-derived (homes), boilerplate
dc2-n-ermineskin-place-agreement	unknown	l	agreement boilerplate, slug ambiguous
dc2-q-chalet-investments-ltd-agreement-c167	unknown	l	agreement boilerplate, slug ambiguous
dc2-r-carreo-condo-agreement	res	l	slug-derived (condo), boilerplate
dc2-s-groveridge-imperial-properties-agreement-c124	unknown	l	agreement boilerplate, slug ambiguous
dc2-t-victoria-trail-condominiums-agreement	res	l	slug-derived (condominiums), boilerplate
dc2-u-groveridge-imperial-properties-agreement-c125	unknown	l	agreement boilerplate, slug ambiguous
dc2-w-beaumaris-road-agreement-c99	unknown	l	agreement boilerplate, slug ambiguous
home	unknown	l	bad URL, no purpose text
"""
DATA = _P1 + _P2 + _P3 + _P4


def parse_labels(raw):
    labels = {}
    for lineno, line in enumerate(raw.splitlines(), 1):
        line = line.rstrip()
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            raise ValueError(f"DATA line {lineno} malformed: {line!r}")
        slug, use, conf = parts[0].strip(), parts[1].strip(), parts[2].strip()
        note = parts[3].strip() if len(parts) > 3 else ""
        if use not in VALID_USES:
            raise ValueError(f"DATA line {lineno}: bad use {use!r} for {slug}")
        if conf not in VALID_CONF:
            raise ValueError(f"DATA line {lineno}: bad conf {conf!r} for {slug}")
        if slug in labels:
            raise ValueError(f"DATA line {lineno}: duplicate slug {slug}")
        labels[slug] = (use, conf, note)
    return labels


def main():
    labels = parse_labels(DATA)
    rows = list(csv.DictReader(open(TEXT_CSV)))
    text_slugs = {r["slug"] for r in rows}
    label_slugs = set(labels)

    missing = text_slugs - label_slugs   # in CSV, no label
    extra = label_slugs - text_slugs     # labelled but not in CSV
    if missing or extra:
        print(f"COVERAGE MISMATCH: {len(missing)} unlabelled, {len(extra)} extra",
              file=sys.stderr)
        if missing:
            print("  unlabelled:", ", ".join(sorted(missing)[:40]), file=sys.stderr)
        if extra:
            print("  extra:", ", ".join(sorted(extra)[:40]), file=sys.stderr)
        sys.exit(1)

    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["slug", "agreement_no", "url", "use", "confidence", "note"])
        for r in sorted(rows, key=lambda x: x["slug"]):
            use, conf, note = labels[r["slug"]]
            w.writerow([r["slug"], r.get("agreement_no", ""), r.get("url", ""),
                        use, conf, note])

    from collections import Counter
    uc = Counter(v[0] for v in labels.values())
    cc = Counter(v[1] for v in labels.values())
    print(f"Wrote {len(rows)} labels -> {os.path.relpath(OUT_CSV, ROOT)}")
    print("  by use:", dict(sorted(uc.items())))
    print("  by confidence:", dict(sorted(cc.items())))


if __name__ == "__main__":
    main()
