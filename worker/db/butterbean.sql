--
-- PostgreSQL database dump
--

-- Dumped from database version 11.16 (Ubuntu 11.16-1.pgdg20.04+1)
-- Dumped by pg_dump version 13.3

-- Started on 2022-06-14 00:22:23

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 3939 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

--
-- TOC entry 196 (class 1259 OID 381630)
-- Name: approved_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.approved_users (
    username character varying(100)
);


ALTER TABLE public.approved_users OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 381633)
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    post_name character varying(100),
    link character varying(100)
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- TOC entry 3932 (class 0 OID 381630)
-- Dependencies: 196
-- Data for Name: approved_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.approved_users (username) FROM stdin;
iTuna#0209
Carissa#0420
hugs#2593
ash#0666
LavenderGrooms#8008
Tupperward#5115
Jackapedia#1612
\.


--
-- TOC entry 3933 (class 0 OID 381633)
-- Dependencies: 197
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (post_name, link) FROM stdin;
goodparenting	https://ibb.co/9c2Nj9c
'sixtynine'	 'https://imgur.com/a/4qIriF2'
'ass'	 'https://imgur.com/a/qkAB9tM'
'butterbean'	 'https://imgur.com/a/n5M5co9'
'didideath'	 'https://imgur.com/a/Narr9EX'
'elidelete'	 'https://imgur.com/a/Lwbt1cW'
'elismoltz'	 'https://imgur.com/a/Lwbt1cW'
'elistorm'	 'https://imgur.com/a/gAPWP0t'
'elitoilet'	 'https://imgur.com/a/0T5OC3I'
'clamshero'	 'https://imgur.com/a/mlYLKKa'
'kathfeet'	 'https://imgur.com/a/pEeHwfh'
'mmhbot'	 'https://imgur.com/a/Hcjhwne'
'backnine'	 'https://imgur.com/a/FiCjgGS'
'smoltzmojo'	 'https://imgur.com/a/KVLMtMv'
'stevefuck'	 'https://imgur.com/a/El3vK4r'
'stevestab'	 'https://imgur.com/a/P2JvBjP'
'smoltzstupid'	 'https://imgur.com/a/5kKqOXH'
thegirlreadingthis	https://imgur.com/OKjMqx2
tweets	https://twitter.com/JungleClams/status/1136709154741997568?s=20
'tuppdoc'	 'https://imgur.com/a/dL9xH7z'
'wattba'	 'https://imgur.com/a/6dljGKC'
'smoltzchest'	 'https://imgur.com/a/LrNpKL3'
'dongbong'	 'https://imgur.com/a/giJFsdW'
'moonpie'	 'https://imgur.com/a/39lnoeP'
'smoltzrise'	 'https://imgur.com/a/jv48kzq'
'banner'	 'https://imgur.com/a/uyPzkzR'
'knockout'	 'https://imgur.com/a/L7FIYPZ'
'beanos'	 'https://imgur.com/a/KRopvrH'
'rip'	 'https://imgur.com/a/gJXq0oF'
'owned'	 'https://imgur.com/tcEbsjq'
'cumwars'	 'https://imgur.com/5Oj8nm9'
buechsreaction	https://imgur.com/W0jhDmz
'yeaboi'	 'https://imgur.com/OehgFA5'
'willieroll'	 'https://imgur.com/efF4klJ'
'blood'	 'https://imgur.com/Vwix320'
'stuffed'	 'https://imgur.com/3cn6quC'
'potw'	 'https://imgur.com/fKR8WKI'
'hooboy'	 'https://imgur.com/ifuncRl'
tarot	!tarot
'shenyun'	 'https://imgur.com/brN1hLP'
'angery'	 'https://imgur.com/OG09tqt'
nice	https://imgur.com/b2Uzbau
'green'	 'https://assets.amuniversal.com/86a4d9802568013788ae005056a9545d'
picture	https://imgur.com/a/xIskr14
'wetthighs'	 'https://imgur.com/XVdteLs'
tucker	https://youtu.be/GLqIB0h1vwY
'mindblown'	 'https://imgur.com/BCN7kCQ'
'yes'	 'https://imgur.com/yRqIs7q'
'grittyyes'	 'https://imgur.com/v5MwA33'
'batromance'	 'https://youtu.be/7ZgdEnS4tdo'
'jimmy'	 'https://youtu.be/Q0hr8X2a2cc'
'corybooker'	 'https://imgur.com/lxWOokW'
gavel	https://imgur.com/a/M0YjjUT
'nutmonth'	 'https://imgur.com/O8RRjIJ'
'fuckduke'	 'https://imgur.com/r70p4rB'
'mildinconvenience'	 'https://imgur.com/QU0lu0Q'
'sip'	 'https://imgur.com/L8X4Pef'
'ham'	 'https://imgur.com/iBr4xsb'
'yike'	 'https://imgur.com/CxujlYQ'
'boomerass'	 'https://imgur.com/1btK9uI'
'hornypatrol'	 'https://imgur.com/JwPNrRI'
'random'	 'Heathcliff random random comment'
'onething'	 'https://www.youtube.com/watch?v=1Q-U2THOF00'
'hpu'	 'https://i.imgur.com/062ammM.png'
'girls'	 'https://imgur.com/vjrgb3F'
'fists'	 'https://imgur.com/vMMOe7E'
'papabless'	 'https://imgur.com/SBqqHuX'
homeboy	https://imgur.com/a/WZBqWEP
report	https://imgur.com/a/1V3XUgP
'gamers'	 'https://imgur.com/BMWS0sh'
'borb'	 'https://imgur.com/aV3FWcu'
'phatt'	 'https://imgur.com/8GJbZZX'
'glad'	 'https://imgur.com/ERArFac'
'cybersteve'	 'https://imgur.com/Tsc6CGi'
'nonono'	 'https://media.tenor.com/images/7b6c8ac5b730a31f45ea234789c1ef17/tenor.gif'
'yesfecta'	 'https://imgur.com/hE2sk0k'
'chefkiss'	 'https://pbs.twimg.com/media/DdSOrwJUQAAfI9e.jpg'
'marianne'	 'https://imgur.com/8nrgiKg'
chachapost	https://imgur.com/a/bQPRJd8
bullshit	https://imgur.com/a/inlvP4e
'jeff'	 'https://imgur.com/Nt3WooR'
'cbt'	 'https://imgur.com/rL4DgNc'
'chuck'	 'https://imgur.com/OoEAfgn'
'oops'	 'https://imgur.com/0qrkudt'
'duality'	 'https://imgur.com/SODqLvi'
'thiccthunk'	 'https://i.boring.host/1153cNgf.png'
tunamorning	https://imgur.com/a/dtzLGDy
'blowout'	 'https://imgur.com/A4VxLjc'
'fridaynight'	 'https://twitter.com/cat_beltane/status/1123424177023746049'
'turdthoughts'	 'https://imgur.com/yJWsuQb'
'mods'	 'https://i.imgur.com/LRV6mQX.png'
'doodoo'	 'https://i.imgur.com/ZluUra3.png'
'fight'	 'https://i.imgur.com/Kq9Tw85.png'
'thisdiscord'	 'https://imgur.com/xeciLwq'
'politics'	 'https://imgur.com/i9V802Q'
'throwup'	 'https://i.imgur.com/UXid6Vc.png'
'fetlife'	 'https://imgur.com/OLGzBYD'
'disgust'	 'https://imgur.com/zyLiEaP'
'riakkuma'	 'https://i.imgur.com/oUh4RFk.png'
'coolthink'	 'https://i.imgur.com/dXi1Q9u.png'
'pigs'	 'https://imgur.com/PdfA1Lc'
'get'	 'https://pbs.twimg.com/media/EAaD2pGWkAAm3bC?format=jpg&name=small'
'blocktuna'	 'https://imgur.com/dW654Mq'
crab	https://imgur.com/SP9JLxk
praxis	https://i.imgur.com/1d2UNhS.png
kofie	https://i.imgur.com/TyBAw4M.png
unpack	https://i.imgur.com/12ZqKBN.jpg
stephen	https://i.imgur.com/oszDPNY.png
italian	https://i.imgur.com/WlFzkmf.png
homer	https://i.imgur.com/Rba6HlS.png
bb	https://imgur.com/14Zi9FW
wish	https://i.imgur.com/tDLMxut.png
silencecrab	https://imgur.com/XJsM2GV
overkill	https://imgur.com/uxF2r9Z
brad	https://i.imgur.com/TRFz6xD.jpg
dragula	https://youtu.be/EqQuihD0hoI
tuppnut	https://i.imgur.com/e7IMlZp.png
empathy	https://i.imgur.com/xB9Os9k.jpg
matty	https://i.imgur.com/SZSNjYm.png
pete	https://youtu.be/5-UrFiz3nwI
beep	meatball
meatball	https://i.imgur.com/2USGlDq.png
beephole	https://imgur.com/Kuu4PJP
pee	https://media.discordapp.net/attachments/465938202503413771/609470566138904576/image0.jpg
newhobby	https://imgur.com/a/NF5ABXc
columbo	https://imgur.com/a/I7dYt52
yang	https://youtu.be/K1jUJ-2MsdA
awesomeface	https://media.tenor.com/images/55ce2e51387e26d301c4a51f1f01ce9d/tenor.gif
wasntfinished	https://i.imgur.com/v6hNlov.jpg
godiva	https://twitter.com/nickciarelli/status/1087412135066427392
subway	https://i.imgur.com/FVzfHj9.png
wolf	https://imgur.com/w46nLQj
contempt	https://i.imgur.com/jIdQrLS.png
khive	https://i.redd.it/a8arw9dvqrs21.jpg
mikeface	https://i.imgur.com/wvPBcck.png
handsome	https://pbs.twimg.com/media/EBjAmSzXUAE9JBU?format=jpg&name=900x900
cretins	https://imgur.com/a/WYxRYB8
bglobby	https://imgur.com/a/XiFewQv
8	https://tenor.com/view/star-wars-bb8-rollin-gif-4826503
salami	https://imgur.com/z5yxcyG
tear	https://i.imgur.com/Uqdumz6.png
bed	https://i.imgur.com/0yR3pbv.png
liam	https://tenor.com/3Yxn.gif
impact	https://imgur.com/DfqEIxz
football	https://i.imgur.com/Y0JmP69.png
defeat	https://imgur.com/cUMdhMH
rat	https://imgur.com/LSjNpnD
eyes	https://i.imgur.com/WJGprMp.png
pizzarat	https://imgur.com/TMHRcrA
mixed	https://i.imgur.com/OanECEO.png
optimus	https://i.imgur.com/xI9yt48.gif
squad	https://imgur.com/SxsO6Se
board	https://i.imgur.com/9yiRJyA.png
slamders	https://imgur.com/nqgD3OB
localman	https://imgur.com/VcsSTk7
garflush	https://imgur.com/On709gu
smug	https://imgur.com/ctlwJ3s
tommyleejones	https://imgur.com/VfUXoDl
joker	https://i.imgur.com/B2Wuu8U.png
bad	https://imgur.com/VFaDAE8
gd	https://i.imgur.com/EkwPJ0G.png
baby	https://i.imgur.com/IzB1eL9.jpg
dodged	https://imgur.com/oqaR6CJ
guess	https://i.imgur.com/dbCYuox.png
stevethumb	https://i.imgur.com/TW18TaL.png
antigd	https://i.imgur.com/kk4jVLp.png
hogwarts	https://imgur.com/a/sYh7n93
garfield	https://i.imgur.com/lCqcLrR.png
order	https://i.imgur.com/BGR8Zmi.png
spray	https://i.imgur.com/OUOAar7.png
theacuck	https://imgur.com/Qc6KjLG
gorbage	https://i.imgur.com/HNISraI.jpg
pattyvoice	https://imgur.com/AZlzEUo
nuclearoption	https://i.imgur.com/ZBm2xHo.png
uber	https://twitter.com/robwhisman/status/735281634656669696
gamers2	https://imgur.com/KN9vVyu
miamad	https://i.imgur.com/6NPL4nJ.png
partyvoice	https://i.imgur.com/JUIW2gv.png
starfish	https://i.imgur.com/lT7113p.png
lisavoice	https://i.imgur.com/lCpXr6y.png
tuppsmell	https://i.imgur.com/QhbbgVi.png
cumdad	https://i.imgur.com/GQ9aAXB.jpg
bab	https://i.imgur.com/E4bukZr.png
jack	https://i.imgur.com/E4bukZr.png
teefhtak	https://i.imgur.com/8fVQo02.png
puzzle	https://i.imgur.com/wkMootm.png
cube	https://i.imgur.com/UDlf6TS.png
when	https://imgur.com/a/GttXOmT
jackplug	https://www.jackapedia.design/
idolcon	https://www.theidolcon.com/
steveplug	https://stephenalcala.com/
lmm	https://i.imgur.com/v654Jf8.png
guy	https://imgur.com/Jg3VUoE
dudestop	https://i.imgur.com/AuJgWL3.png
a+	https://i.imgur.com/W1cdjmu.png
yupp	https://imgur.com/ffuYCMY
yeababy	https://imgur.com/Ry5hbNI
contempt	https://i.imgur.com/w4pliwq.png
pedal	https://i.imgur.com/8YLHzm8.png
contentment	https://imgur.com/yUq2QCk
smackwetz	https://imgur.com/vN3Z5zt
miapiss	https://i.imgur.com/KdEAFNq.png
\.


--
-- TOC entry 3940 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM postgres;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- TOC entry 3941 (class 0 OID 0)
-- Dependencies: 596
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO postgres;


-- Completed on 2022-06-14 00:22:25

--
-- PostgreSQL database dump complete
--

