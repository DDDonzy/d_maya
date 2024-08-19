//Maya ASCII 2016 scene
//Name: fit_sh.ma
//Last modified: Fri, Sep 07, 2018 05:21:26 PM
//Codeset: 936
requires maya "2016";
requires -nodeType "ilrOptionsNode" -nodeType "ilrUIOptionsNode" -nodeType "ilrBakeLayerManager"
		 -nodeType "ilrBakeLayer" "Turtle" "2016.0.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2016";
fileInfo "version" "2016";
fileInfo "cutIdentifier" "201603180400-990260";
fileInfo "osv" "Microsoft Windows 8 , 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "9CD57C7D-4E05-AA3B-F55F-9CAC801B7FAC";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 22.80020913725064 5.0806638907556607 22.020891746847113 ;
	setAttr ".r" -type "double3" -2.7383527296190864 54.199999999998234 -3.3982743725143157e-016 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "5CE63E11-4581-6F62-3883-A58536655403";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 28.143622599786688;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 3.7361001140814438 5.5768622957876266 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "AFBFA34F-4BA6-2BA6-B7F8-6194F3198FC7";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "AF80F050-4946-0EA2-49EB-ED8458C14931";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "B557D8E3-4320-3B3F-3DC6-81BAEE67E50B";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "011A3685-41FB-B80E-A7E9-A49F65FE691C";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "3521BD4D-4B70-5406-682E-9A9EEAEA6E92";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.20339202189574 4.6156555114752065 5.5816828367518259 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "29F60E08-4B7F-C759-4FD2-D1A53C7BCBB8";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 23.896824219085499;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "Facial_Skeleton_GRP";
	rename -uid "14532B1E-4B98-06CA-A812-0EA2A6A87722";
createNode transform -n "M_Head_Position" -p "Facial_Skeleton_GRP";
	rename -uid "02737119-4A52-0A60-805E-1EA850325686";
	addAttr -ci true -sn "faceGeo" -ln "faceGeo" -dt "string";
	addAttr -ci true -sn "eyeBallGeo" -ln "eyeBallGeo" -dt "string";
	addAttr -ci true -sn "teethUpperGeo" -ln "teethUpperGeo" -dt "string";
	addAttr -ci true -sn "teethLowerGeo" -ln "teethLowerGeo" -dt "string";
	addAttr -ci true -sn "tongueGeo" -ln "tongueGeo" -dt "string";
	addAttr -ci true -sn "allOtherGeo" -ln "allOtherGeo" -dt "string";
	setAttr -k on ".faceGeo" -type "string" "";
	setAttr -k on ".eyeBallGeo";
	setAttr -k on ".teethUpperGeo";
	setAttr -k on ".teethLowerGeo";
	setAttr -k on ".tongueGeo";
	setAttr -k on ".allOtherGeo";
createNode locator -n "M_Head_PositionShape" -p "M_Head_Position";
	rename -uid "752FD438-40FE-3CD3-CE45-2D8F6DC06616";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".los" -type "double3" 10 10 10 ;
createNode joint -n "M_Head_Skeleton" -p "M_Head_Position";
	rename -uid "6C75619B-48D9-C29F-B580-FBBAC5C2A256";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 6.7213108154266488 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 3.180554681463516e-015 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 6.7213108154266488 0 1;
	setAttr ".radi" 5.3000000000000007;
createNode joint -n "M_HeadUpper_Skeleton" -p "M_Head_Skeleton";
	rename -uid "95ABC778-4B32-D299-F325-C080E482C685";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 1.0968275696131364 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 3.180554681463516e-015 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 7.8181383850397852 0 1;
	setAttr ".radi" 2;
createNode transform -n "HeadUpper_Skeleton_GRP" -p "M_HeadUpper_Skeleton";
	rename -uid "FFA00F9D-4730-6583-06C6-4AB6955C0DDD";
	setAttr ".t" -type "double3" 0 -7.8181383850397852 0 ;
createNode transform -n "HeadUpper_None_GRP" -p "HeadUpper_Skeleton_GRP";
	rename -uid "61F07C2D-476D-1277-075A-3D8927D34A92";
createNode joint -n "M_Brow_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "C87067F9-41F2-23B3-B528-139D27DEBEAB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 10.356332568764975 9.1043643951416016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 10.382339477539062 9.1043643951416016 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Brow_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "2343ED8D-4E87-279F-AAFD-6EAC20AE4A2F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.4691572189331055 10.356332568764975 9.0161819458007812 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 0 0 0 0 1 0 0 0 0 1 0 1.4691572189331055 10.356332568764975 9.0161819458007812 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Brow_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "F4895D69-4204-F2DA-EF07-9193F1F7BAF5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.2037782669067383 10.572027206420898 8.592747688293457 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 0 0 0 0 1 0 0 0 0 1 0 3.2037782669067383 10.572027206420898 8.592747688293457 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Brow_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "E8AF6ABB-4182-E142-6E4F-2E9328B128CC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.7354907989501953 10.53758430480957 7.5964393615722656 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 0 0 0 0 1 0 0 0 0 0.99999999999999989 0
		 4.7354907989501953 10.53758430480957 7.5964393615722656 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Brow_03_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "F12DD899-4944-C82F-02F4-1EBB4040E51A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.8503628894613122 10.3752855238635 5.9211162469652514 ;
	setAttr ".s" -type "double3" 1 1 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 0.99999999999999989 0 5.8503628894613122 10.3752855238635 5.9211162469652514 1;
	setAttr ".radi" 0.55;
createNode joint -n "M_NoseBridge_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "6D805348-4B14-23F7-FEC0-4493ACA0028D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 8.3340854644775391 8.7626216251277107 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 8.3340854644775391 8.7626216251277107 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_SocketInner_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "4D7E90D9-4D91-CEAC-D17B-77A1D001340C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.2401901235847823 8.4420241746844233 8.0583465244996688 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3782232003889379 8.2179290344994254 8.058346524499667 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_SocketUpper_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "BB4203F1-4C79-010C-C4AB-64B2A2235E7D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0917415618896484 9.171689226019371 8.280426025390625 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.9497871398925781 9.4036388397216797 8.280426025390625 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_SocketUpper_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "36E63352-43F1-B4A9-F337-C0B68AB4749B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.3179900646209717 9.171689226019371 8.0734004974365234 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.3550353050231934 9.7519245147705078 8.0734004974365234 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_SocketUpper_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "C80309AA-4157-B236-E813-77879BE33F92";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.4987268447875977 9.171689226019371 7.3598788098301382 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.6270670890808105 9.7465419769287109 7.1343746185302734 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_SocketOuter_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "A13AF4A8-4CBD-9AA4-24C1-D2986F6A0FEA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.2656780232713203 8.437317747507258 6.3903667231273822 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 5.0318503379821777 9.2830460438015887 6.3610515594482422 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_SocketLower_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "357DC594-44FD-4444-462F-369BBBB7F860";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0934193134307861 7.71017785963177 7.840672492980957 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0820850144959206 7.7015838623046875 7.840672492980957 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_SocketLower_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "F8876885-473B-7E57-BF40-268F2BD2D917";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.3083300590515137 7.71017785963177 7.6035885810852051 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.2839744577947449 7.4680519104003906 7.6035885810852051 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_SocketLower_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "BBEF318C-4017-9E54-B76D-248DA94C2E14";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.4987268447875977 7.71017785963177 7.0099451855625601 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.6187248229980469 8.0747470855712891 6.7844409942626953 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LidInner_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "512D2712-45AF-017B-0E3A-CE89253CDE87";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6553013324737549 8.437317747507258 7.8856148719787598 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.6553013324737549 8.2814254760742187 7.8856148719787598 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LidUpper_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "5958887C-48CD-C753-5040-789297197E24";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0917415618896484 8.615190713301752 8.0394248962402344 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0917415618896484 8.4562473297119141 8.0394248962402344 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LidUpper_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "B8BF6F9A-4116-AC54-3DD7-51944DE7D4B2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.3179900646209717 8.615190713301752 7.9887332916259766 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 0 0 0 0 1 0 0 0 0 1 0 3.3179900646209717 8.7515964508056641 7.9887332916259766 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LidUpper_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "B69C6685-4DC8-187C-E974-EB9F8D1BA474";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.4987268447875977 8.615190713301752 7.2066859685625948 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 0 0 0 0 0.99999999999999989 0 0
		 0 0 1 0 4.4987268447875977 9.1129188537597656 7.1400823593139648 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LidOuter_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "DFC27BAF-4BD3-60EB-4195-9FB91356D146";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.876265968638287 8.437317747507258 6.7999181648650051 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.8247900009155273 9.2105464935302734 6.5966176986694336 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LidLower_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "DD33E28B-4FCC-E84F-A00E-BE84411E848C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0934193134307861 8.2652094053183536 7.9774303436279297 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0934193134307861 8.2320842742919922 7.9774303436279297 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LidLower_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "E9329EBA-4D72-0A93-E8FB-D194863ED28B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.3083300590515137 8.2652094053183536 7.9009857177734375 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.3083300590515137 8.4016151428222656 7.9009857177734375 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LidLower_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "AB28D2AF-439A-35AD-2F5A-638F4D6D77F1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.4987268447875977 8.2652094053183536 7.1507586919512667 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.514655590057373 8.8801898956298828 7.0841550827026367 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Orbit_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "B5621936-43C7-EA29-FFEB-70BF89017260";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5547847747802734 7.1849288940429687 8.1608667373657227 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.5547847747802734 7.1849288940429687 8.1608667373657227 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Orbit_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "231D0663-4B90-D90B-5488-2D9FD70C7075";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.9833431243896484 6.4433689117431641 7.890528678894043 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.9833431243896484 6.4433689117431641 7.890528678894043 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Orbit_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "C1DD2F86-41D9-24A9-ADC8-0C8FE0E5D3BB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.4723429679870605 6.6044464111328125 6.7346591949462891 ;
	setAttr ".s" -type "double3" 1 0.99999999999999989 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99999999999999989 0 0 0 0 0.99999999999999989 0
		 4.4723429679870605 6.6044464111328125 6.7346591949462891 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Orbit_03_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "1FA63F81-4BF7-F75E-2D8A-3CAEAEB888C5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.333162784576416 7.5637702941894531 5.7535190582275391 ;
	setAttr ".s" -type "double3" 1 0.99999999999999978 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99999999999999978 0 0 0 0 0.99999999999999989 0
		 5.333162784576416 7.5637702941894531 5.7535190582275391 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Brow_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "B9FE097A-4A09-4A40-4FE7-F59C527CDECF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.4691572189331055 10.356332568764975 9.0161819458007812 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -0.99999999999999989 0 -1.224646799147353e-016 0 0 1 0 0
		 1.2246467991473532e-016 0 -1 0 -1.4691572189331055 10.356332568764975 9.0161819458007812 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Brow_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "9F3CF7AA-4AB1-4771-5591-3EA46309818A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.2037782669067383 10.572027206420898 8.592747688293457 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -0.99999999999999989 0 -1.224646799147353e-016 0 0 1 0 0
		 1.2246467991473532e-016 0 -1 0 -3.2037782669067383 10.572027206420898 8.592747688293457 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Brow_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "C35B0E06-417B-700C-6F1E-E68ED6D47296";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.7354907989501953 10.53758430480957 7.5964393615722656 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -0.99999999999999989 0 -1.224646799147353e-016 0 0 1 0 0
		 1.224646799147353e-016 0 -0.99999999999999989 0 -4.7354907989501953 10.53758430480957 7.5964393615722656 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Brow_03_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "AB087C34-4029-5504-3264-EB843FE2AB6E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.8503628894613122 10.3752855238635 5.9211162469652514 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.224646799147353e-016 0 -0.99999999999999989 0
		 -5.8503628894613122 10.3752855238635 5.9211162469652514 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LidInner_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "662D8F32-4EB5-977F-85D6-06A17200D44F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.6553013324737549 8.437317747507258 7.8856148719787598 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.6553013324737549 8.2814254760742187 7.8856148719787598 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LidLower_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "84053E9D-42BF-0099-AFB0-019477358AB5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0934193134307861 8.2652094053183536 7.9774303436279297 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -2.0934193134307861 8.2320842742919922 7.9774303436279297 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LidLower_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "072C7838-4819-2119-1F6E-1CAFDC5A6769";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.3083300590515137 8.2652094053183536 7.9009857177734375 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -3.3083300590515137 8.4016151428222656 7.9009857177734375 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LidLower_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "C5ADEC74-4520-6483-EDF0-AE818D0ED784";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4987268447875977 8.2652094053183536 7.1507586919512667 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -4.514655590057373 8.8801898956298828 7.0841550827026367 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LidOuter_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "E0115BC1-4C27-35A8-BE9A-2F87B58B37F1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.876265968638287 8.437317747507258 6.7999181648650051 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -4.8247900009155273 9.2105464935302734 6.5966176986694336 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LidUpper_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "110A8C09-486E-BF1A-8462-F5B5ECDF73F6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0917415618896484 8.615190713301752 8.0394248962402344 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -2.0917415618896484 8.4562473297119141 8.0394248962402344 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LidUpper_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "EF6DFE38-47F2-C286-BE45-068F624D65B5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.3179900646209717 8.615190713301752 7.9887332916259766 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -0.99999999999999989 0 -1.224646799147353e-016 0 0 1 0 0
		 1.2246467991473532e-016 0 -1 0 -3.3179900646209717 8.7515964508056641 7.9887332916259766 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LidUpper_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "CE2C603E-4AA3-CA72-B199-07A6B592C0FF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4987268447875977 8.615190713301752 7.2066859685625948 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -0.99999999999999989 0 -1.224646799147353e-016 0 0 0.99999999999999989 0 0
		 1.2246467991473532e-016 0 -1 0 -4.4987268447875977 9.1129188537597656 7.1400823593139648 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Orbit_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "8F5000FB-40DF-B54B-799B-4EA84C444E64";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.5547847747802734 7.1849288940429687 8.1608667373657227 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.5547847747802734 7.1849288940429687 8.1608667373657227 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Orbit_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "201A2C33-4EEF-A6E6-2F43-C88D6FAA26CC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.9833431243896484 6.4433689117431641 7.890528678894043 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -2.9833431243896484 6.4433689117431641 7.890528678894043 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Orbit_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "0464F9A4-4B0B-FB4C-87BC-4790BAAB1528";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4723429679870605 6.6044464111328125 6.7346591949462891 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 0.99999999999999989 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 0.99999999999999989 0 0
		 1.224646799147353e-016 0 -0.99999999999999989 0 -4.4723429679870605 6.6044464111328125 6.7346591949462891 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Orbit_03_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "972E39F4-474E-4640-A3F5-4E9615AA2DDF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.333162784576416 7.5637702941894531 5.7535190582275391 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 0.99999999999999978 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 0.99999999999999978 0 0
		 1.224646799147353e-016 0 -0.99999999999999989 0 -5.333162784576416 7.5637702941894531 5.7535190582275391 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_SocketInner_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "2FE2332F-4D2D-13D5-CB7A-DC9884C1C8C8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.2401901235847823 8.4420241746844233 8.0583465244996688 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.3782232003889379 8.2179290344994254 8.058346524499667 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_SocketLower_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "3369E719-48B9-9F2D-822C-D6BCA6C6D716";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0934193134307861 7.71017785963177 7.840672492980957 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -2.0820850144959206 7.7015838623046875 7.840672492980957 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_SocketLower_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "8AC86D44-4908-6A5C-6FD2-2BB75D55DC0C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.3083300590515137 7.71017785963177 7.6035885810852051 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -3.2839744577947449 7.4680519104003906 7.6035885810852051 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_SocketLower_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "CCE2F019-430B-2C5F-7CFD-57A58F5880B6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4987268447875977 7.71017785963177 7.0099451855625601 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -4.6187248229980469 8.0747470855712891 6.7844409942626953 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_SocketOuter_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "C968AD5E-4CBC-CC3A-B132-668E244E1E46";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.2656780232713203 8.437317747507258 6.3903667231273822 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -5.0318503379821777 9.2830460438015887 6.3610515594482422 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_SocketUpper_00_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "789848F3-4E1E-DFEE-AE3A-79B493868578";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0917415618896484 9.171689226019371 8.280426025390625 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.9497871398925781 9.4036388397216797 8.280426025390625 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_SocketUpper_01_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "F0E1F75C-4199-DB2B-5A7E-8680263CB8D3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.3179900646209717 9.171689226019371 8.0734004974365234 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -3.3550353050231934 9.7519245147705078 8.0734004974365234 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_SocketUpper_02_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "4477E136-4EED-5999-FE85-8D8CB09D9874";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4987268447875977 9.171689226019371 7.3598788098301382 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -4.6270670890808105 9.7465419769287109 7.1343746185302734 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Eye_00_Gross_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "C61B2137-44C4-A540-598E-A2A99D1BD45F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.874 8.8173221255658127 5.7122009164108185 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.5205256903507491 124.11430830406933 8.8751576264219292 1;
	setAttr ".radi" 3;
createNode joint -n "L_EyeBall_00_Skeleton" -p "L_Eye_00_Gross_Skeleton";
	rename -uid "2C7B2D86-42EE-E252-7093-2B8AFC0B3291";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -l on ".v" no;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 180 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.5205256903507491 124.11430830406933 8.8751576264219292 1;
	setAttr ".radi" 2;
createNode joint -n "R_Eye_00_Gross_Skeleton" -p "HeadUpper_None_GRP";
	rename -uid "FB6EA4E6-4B8D-D276-DB00-C98EE93166D5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.874 8.8173221255658127 5.7122009164108185 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.5205256903507491 124.11430830406933 8.8751576264219292 1;
	setAttr ".radi" 3;
createNode joint -n "R_EyeBall_00_Skeleton" -p "R_Eye_00_Gross_Skeleton";
	rename -uid "E9B3BB3E-43DD-BA8A-94CC-86BECCF6234D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -l on ".v" no;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.5205256903507491 124.11430830406933 8.8751576264219292 1;
	setAttr ".radi" 2;
createNode joint -n "M_HeadLower_Skeleton" -p "M_Head_Skeleton";
	rename -uid "EA0ED234-42F4-F8B8-3721-1AA8C6AD53BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 -1.0764664923223961 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 3.180554681463516e-015 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 5.6448443231042527 0 1;
	setAttr ".radi" 2;
createNode transform -n "HeadLower_Skeleton_GRP" -p "M_HeadLower_Skeleton";
	rename -uid "956DA927-401D-F248-5806-A6B823B3360D";
	setAttr ".t" -type "double3" 0 -5.6448443231042527 0 ;
createNode transform -n "HeadLower_None_GRP" -p "HeadLower_Skeleton_GRP";
	rename -uid "FEF90DB0-4CC4-3668-90A9-FAAF87D5AC69";
createNode joint -n "M_JawUpper_Position_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "F218D7C9-4E42-756A-3C77-49A7373CCA7C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 5.6716527584285696 1.8609980322317961 ;
	setAttr ".r" -type "double3" 7.6371600726928177 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".pa" -type "double3" 0 0 3.180554681463516e-015 ;
	setAttr ".bps" -type "matrix" 0 -0.72291967718206462 0.69093208084657609 0 1.1102230246251568e-016 0.69093208084657598 0.72291967718206462 0
		 -1.0000000000000002 0 0 0 -0.1640972039630029 121.38652052672195 3.9390330105855029 1;
createNode joint -n "M_JawUpperEnd_Skeleton" -p "M_JawUpper_Position_Skeleton";
	rename -uid "7C92A178-4335-D5D2-0B26-63A51E2B28AB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 2.2204460492503131e-016 7 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 3.180554681463516e-015 ;
	setAttr ".bps" -type "matrix" 0 -0.72291967718206462 0.69093208084657609 0 1.1102230246251568e-016 0.69093208084657598 0.72291967718206462 0
		 -1.0000000000000002 0 0 0 -0.1640972039630029 121.38652052672195 3.9390330105855029 1;
createNode transform -n "M_TeethUpper_Skeleton_GRP" -p "M_JawUpper_Position_Skeleton";
	rename -uid "36BC6550-4AB1-EB8D-4844-3292569A2930";
	setAttr ".t" -type "double3" 0 -5.8686678805098387 -1.0907318627569209 ;
	setAttr ".r" -type "double3" -7.6371600726928177 0 0 ;
createNode transform -n "M_TeethUpper_None_GRP" -p "M_TeethUpper_Skeleton_GRP";
	rename -uid "2E2C641A-4CC4-A36D-ECFB-A18F7A5BFD3A";
createNode joint -n "M_TeethUpper_00_Skeleton" -p "M_TeethUpper_None_GRP";
	rename -uid "DBA776FB-4BE4-2CA2-A1E0-9BB4ED4AED00";
	setAttr ".t" -type "double3" 0 4.9882382240685486 6.5727718476563508 ;
	setAttr ".r" -type "double3" 13.043803025650517 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.5;
createNode nurbsSurface -n "M_TeethUpper_00_SkeletonShape" -p "M_TeethUpper_00_Skeleton";
	rename -uid "91E1D274-4691-3C1F-053C-D08067F086BF";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 0 no 
		6 0 0 0 1 1 1
		6 0 0 0 1 1 1
		
		16
		-1.05 -6.4293956955236049e-017 1.05
		-1.05 -2.143131898507868e-017 0.34999999999999998
		-1.05 2.1431318985078686e-017 -0.35000000000000009
		-1.05 6.4293956955236049e-017 -1.05
		-0.34999999999999998 -6.4293956955236049e-017 1.05
		-0.34999999999999998 -2.143131898507868e-017 0.34999999999999998
		-0.34999999999999998 2.1431318985078686e-017 -0.35000000000000009
		-0.34999999999999998 6.4293956955236049e-017 -1.05
		0.35000000000000009 -6.4293956955236049e-017 1.05
		0.35000000000000009 -2.143131898507868e-017 0.34999999999999998
		0.35000000000000009 2.1431318985078686e-017 -0.35000000000000009
		0.35000000000000009 6.4293956955236049e-017 -1.05
		1.05 -6.4293956955236049e-017 1.05
		1.05 -2.143131898507868e-017 0.34999999999999998
		1.05 2.1431318985078686e-017 -0.35000000000000009
		1.05 6.4293956955236049e-017 -1.05
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode joint -n "M_JawLower_Position_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "885356F3-4249-754C-4140-559764278CB6";
	setAttr ".t" -type "double3" 0 5.6716527584285696 1.8609980322317961 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 41.235040530762099 0 0 ;
	setAttr ".is" -type "double3" 0.99999999999999978 1 1 ;
createNode joint -n "M_JawLowerEnd_Skeleton" -p "M_JawLower_Position_Skeleton";
	rename -uid "735EFFB2-4A17-0158-1E7C-1C90BDD7183F";
	setAttr ".t" -type "double3" 0 0 7 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 3.180554681463516e-015 0 0 ;
createNode transform -n "M_JawLower_Skeleton_GRP" -p "M_JawLower_Position_Skeleton";
	rename -uid "7EAEDECB-4279-BE6A-FE7D-F595F33DDD40";
	setAttr ".t" -type "double3" 0 -5.4918264570901725 2.3389743165253902 ;
	setAttr ".r" -type "double3" -41.235040530762099 0 0 ;
	setAttr ".s" -type "double3" 0.99999999999999978 1 1 ;
createNode transform -n "M_JawLower_None_GRP" -p "M_JawLower_Skeleton_GRP";
	rename -uid "9ABA6A9F-4F3A-6E9D-7405-2BB7CA2FBCEA";
createNode joint -n "L_JawLine_02_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "E0A22D1B-4316-8D6D-7B7A-0D80DDD4CE47";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.6366920471191406 3.0374965667724609 2.3502998352050781 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.6366920471191406 3.0374965667724609 2.3502998352050781 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_JawLine_01_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "E53D99DB-4482-BEEA-1F1C-BDB9F44D711B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.6291710926439311 2.1254276564029988 4.0004947173865943 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.6291710926439311 2.1692889871743195 4.0004947173865943 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_JawLine_00_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "C28E0A08-4AE6-3DC8-DA45-5C909D2E4DF3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.9805426546013161 1.2296630427961142 5.602295934346035 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.9805426546013161 1.1638710466391315 5.602295934346035 1;
	setAttr ".radi" 0.55;
createNode joint -n "M_Chin_00_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "B86DCF87-4360-58B6-396E-8099A0E94EE2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 0.58954048156738281 7.0004043579101563 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0.58954048156738281 7.0004043579101563 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_JawLine_00_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "DCF58494-4AE4-802E-5BB2-78BE6DF18B13";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.9805426546013161 1.2296630427961142 5.602295934346035 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.9805426546013161 1.1638710466391315 5.602295934346035 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_JawLine_01_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "6FFE3A4A-49DA-5A1B-5C9A-11BF0EB4CCC4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.6291710926439311 2.1254276564029988 4.0004947173865943 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -3.6291710926439311 2.1692889871743195 4.0004947173865943 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_JawLine_02_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "1A7CCDE4-4776-B904-0136-BAA05928D33F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.6366920471191406 3.0374965667724609 2.3502998352050781 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 3.0374965667724609 2.3502998352050781 1;
	setAttr ".radi" 0.55;
createNode joint -n "M_Throat_00_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "84089535-4DC6-0200-A105-9B9140EE6252";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 0.20410917876077495 3.4068894386291513 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3018839359283447 121.86194610595706 11.93608570098877 1;
	setAttr ".radi" 0.55;
createNode joint -n "M_Tongue_00_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "293A76A2-4477-5B4C-ED6A-5492A9EEA6D1";
	setAttr ".t" -type "double3" 0 3.9881726906063659 3.5004789942463228 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".jo" -type "double3" -21.741840498025237 0 0 ;
	setAttr ".radi" 0.51501565024724738;
createNode joint -n "M_Tongue_01_Skeleton" -p "M_Tongue_00_Skeleton";
	rename -uid "C537C1CE-4C61-ADA4-4F71-50819E262D10";
	setAttr ".t" -type "double3" 0 -0.07023887065179002 1.4858902122038531 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".jo" -type "double3" 21.980237616068532 0 0 ;
	setAttr ".radi" 0.51234054026840403;
createNode joint -n "M_Tongue_02_Skeleton" -p "M_Tongue_01_Skeleton";
	rename -uid "3D9587A7-4D17-7E6C-A786-F6A2E5CCA9B1";
	setAttr ".t" -type "double3" 1.4014409875282513e-016 -0.043189280658444851 1.3947514888273087 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".jo" -type "double3" 13.70463071350806 0 0 ;
	setAttr ".radi" 0.5;
createNode joint -n "M_Tongue_03_Skeleton" -p "M_Tongue_02_Skeleton";
	rename -uid "70696E77-4C12-1B4C-D863-89AD6F39C9CF";
	setAttr ".t" -type "double3" 2.4339011095663331e-017 -0.038771555890341425 1.0949099946781136 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".jo" -type "double3" 12.383112058393634 0 0 ;
	setAttr ".radi" 0.5;
createNode joint -n "M_Tongue_04_Skeleton" -p "M_Tongue_03_Skeleton";
	rename -uid "8589A15F-4061-CE33-FAD3-50992C8DDF38";
	setAttr ".t" -type "double3" 3.1280248912711394e-016 -0.024631621574261686 0.94144624385795073 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".jo" -type "double3" 8.1907348004978164 0 0 ;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".radi" 0.5;
createNode joint -n "M_TeethLower_00_Skeleton" -p "M_JawLower_None_GRP";
	rename -uid "E206FE05-4F72-404D-0DF0-7FA7277CA70A";
	setAttr ".t" -type "double3" 0 3.8290264401873992 6.3023708221125823 ;
	setAttr ".r" -type "double3" 14.200930774704791 0 0 ;
	setAttr -av ".rx";
	setAttr -av ".ry";
	setAttr -av ".rz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.5;
createNode nurbsSurface -n "M_TeethLower_00_SkeletonShape" -p "M_TeethLower_00_Skeleton";
	rename -uid "941994D4-49C6-09D2-C982-4BAADFBE1E65";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 0 no 
		6 0 0 0 1 1 1
		6 0 0 0 1 1 1
		
		16
		-1.05 -6.4293956955236049e-017 1.05
		-1.05 -2.143131898507868e-017 0.34999999999999998
		-1.05 2.1431318985078686e-017 -0.35000000000000009
		-1.05 6.4293956955236049e-017 -1.05
		-0.34999999999999998 -6.4293956955236049e-017 1.05
		-0.34999999999999998 -2.143131898507868e-017 0.34999999999999998
		-0.34999999999999998 2.1431318985078686e-017 -0.35000000000000009
		-0.34999999999999998 6.4293956955236049e-017 -1.05
		0.35000000000000009 -6.4293956955236049e-017 1.05
		0.35000000000000009 -2.143131898507868e-017 0.34999999999999998
		0.35000000000000009 2.1431318985078686e-017 -0.35000000000000009
		0.35000000000000009 6.4293956955236049e-017 -1.05
		1.05 -6.4293956955236049e-017 1.05
		1.05 -2.143131898507868e-017 0.34999999999999998
		1.05 2.1431318985078686e-017 -0.35000000000000009
		1.05 6.4293956955236049e-017 -1.05
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode joint -n "M_LipUpper_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "EC9EF99C-489A-2BD4-B52F-79ACC7A6D271";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 4.0269913673400879 8.9925823211669922 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 4.0269913673400879 8.9925823211669922 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LipUpper_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "02C0D3D7-4114-3DE5-5E76-A2B00C2E85A5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.54260778427124023 4.028529167175293 8.8784980773925781 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.54260778427124023 4.028529167175293 8.8784980773925781 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LipUpper_01_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "CED60A1D-47FB-259B-4DF6-72A6CA003EBA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.0074524879455566 4.0015859603881836 8.5875701904296875 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.0074524879455566 4.0015859603881836 8.5875701904296875 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LipUpper_02_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "616EC2CC-48BA-B31A-4EC1-E08F62453FCB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.4180364608764648 3.9101667404174805 8.1984710693359375 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.4180364608764648 3.9101667404174805 8.1984710693359375 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LipConner_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "0C20B66C-4F99-FDFC-C40A-DEAD4CE535A2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6381075382232666 3.789484977722168 7.848480224609375 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.6381075382232666 3.789484977722168 7.848480224609375 1;
	setAttr ".radi" 0.55;
createNode joint -n "M_LipLower_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "06CAAF3A-4FD9-AC1E-9CAC-E28642C283C8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 3.4986839294433594 8.8420066833496094 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 3.4986839294433594 8.8420066833496094 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LipLower_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "C41D406E-4B56-62F7-EDFE-1DABB31C8BA1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.61316394805908203 3.5082130432128906 8.7187004089355469 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.61316394805908203 3.5082130432128906 8.7187004089355469 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LipLower_01_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "BA2D6D00-4BCA-4228-8C3C-109ECAE2E55F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.0965092182159424 3.5773906707763672 8.4012517929077148 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.0965092182159424 3.5773906707763672 8.4012517929077148 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_LipLower_02_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "0377AEF4-40BC-321B-96F9-F89461347066";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.4596633911132812 3.6742439270019531 8.0475120544433594 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.4596633911132812 3.6742439270019531 8.0475120544433594 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_MouthUpper_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "41C830C5-4629-5790-9C36-E7A99100FBA7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.2832523584365845 6.3339557647705078 8.5894432067871094 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.2832523584365845 6.3339557647705078 8.5894432067871094 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_MouthUpper_01_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "9EFE59F9-406C-0252-BC00-BBB611445592";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.1263527870178223 5.1193389892578125 8.1643352508544922 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.1263527870178223 5.1193389892578125 8.1643352508544922 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_MouthConner_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "46BFF2AB-4040-24A5-E56F-EEAFBD4A544B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.3640142343991828 3.9333019256591797 7.6348066329956064 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3640142343991828 3.9333019256591797 7.6348066329956064 1;
	setAttr ".radi" 0.55;
createNode joint -n "M_MouthLower_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "77260404-4683-2C9A-B0CC-F5B92ABCCFBD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 1.8350624279599814 7.6724090284968298 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 1.8350624279599814 7.6724090284968298 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_MouthLower_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "1F15CCC2-40E8-8922-A8D3-FFA342427FA8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1348832059433636 2.0061206817626953 7.3398809432983398 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1348832059433636 2.0061206817626953 7.3398809432983398 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_MouthLower_01_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "BF831A5E-4BD2-FB93-90EF-678420A01B27";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0158705354273443 2.7136820426164658 7.1741893847108393 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0158705354273443 2.7136820426164658 7.1741893847108393 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_Cheek_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "A20AF31D-4883-58A8-DA35-808220BACBA4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.4622001647949219 4.5758880849462509 6.0692009925842285 ;
	setAttr ".r" -type "double3" 8.7465253740246703e-015 1.1927080055488187e-014 3.1805546814635176e-015 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 0 0 0 0 1 0 0 0 0 0.99999999999999989 0
		 5.084636688232421 119.46546173095703 10.099560737609872 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_Cheek_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "AA8D990A-40E7-CDCB-A250-9084A89A1339";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4622001647949219 4.5758880849462509 6.0692009925842285 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 0.99999999999999989 1 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 0 0 0 0 1 0 0 0 0 0.99999999999999989 0
		 5.084636688232421 119.46546173095703 10.099560737609872 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LipLower_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "7AA11E6D-4D17-CB4D-DC4C-D0AC87ED2F67";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.61316394805908203 3.5082130432128906 8.7187004089355469 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -0.61316394805908203 3.5082130432128906 8.7187004089355469 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LipLower_01_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "9160B6EB-4052-742A-8FA0-0299B40F5694";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.0965092182159424 3.5773906707763672 8.4012517929077148 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.0965092182159424 3.5773906707763672 8.4012517929077148 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LipLower_02_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "D0ADC6E8-4F6F-77FF-D31C-EFA0FC465C7D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.4596633911132812 3.6742439270019531 8.0475120544433594 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.4596633911132812 3.6742439270019531 8.0475120544433594 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LipConner_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "D23C6246-4CB2-8542-E525-298D0F5FDB0B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.6381075382232666 3.789484977722168 7.848480224609375 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.6381075382232666 3.789484977722168 7.848480224609375 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LipUpper_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "3BDFFA03-4D06-F354-BCF3-44A9A04C41E8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.54260778427124023 4.028529167175293 8.8784980773925781 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -0.54260778427124023 4.028529167175293 8.8784980773925781 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LipUpper_01_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "40A3E019-44FC-B3E7-84F8-48A3ACA2BFE6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.0074524879455566 4.0015859603881836 8.5875701904296875 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.0074524879455566 4.0015859603881836 8.5875701904296875 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_LipUpper_02_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "E1537C19-4B1E-0035-6D9F-DFA1E93D4EFF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.4180364608764648 3.9101667404174805 8.1984710693359375 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.4180364608764648 3.9101667404174805 8.1984710693359375 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_MouthConner_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "514B3075-4652-CD3B-2917-C7AA9F49F0CD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.3640142343991828 3.9333019256591797 7.6348066329956064 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -2.3640142343991828 3.9333019256591797 7.6348066329956064 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_MouthLower_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "AB450A53-43BB-4A32-E367-7B9256C1EEEF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.1348832059433636 2.0061206817626953 7.3398809432983398 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.1348832059433636 2.0061206817626953 7.3398809432983398 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_MouthLower_01_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "3B4C591D-4349-8C19-1DD1-C2A429B27765";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0158705354273443 2.7136820426164658 7.1741893847108393 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -2.0158705354273443 2.7136820426164658 7.1741893847108393 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_MouthUpper_00_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "D390AF8C-47C6-D13C-ED70-20B11A66CA06";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.2832523584365845 6.3339557647705078 8.5894432067871094 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -1.2832523584365845 6.3339557647705078 8.5894432067871094 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_MouthUpper_01_Skeleton" -p "HeadLower_None_GRP";
	rename -uid "388E2C1E-43E5-D1B3-D08A-31AD519EA859";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.1263527870178223 5.1193389892578125 8.1643352508544922 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-016 0 0 1 0 0 1.2246467991473532e-016 0 -1 0
		 -2.1263527870178223 5.1193389892578125 8.1643352508544922 1;
	setAttr ".radi" 0.55;
createNode transform -n "TeethUpper_Second_GRP" -p "HeadLower_None_GRP";
	rename -uid "23F2175B-48C0-CB9D-AE10-A38258715110";
	setAttr -l on ".v" no;
createNode joint -n "M_TeethUpper_Sec_00_Skeleton" -p "TeethUpper_Second_GRP";
	rename -uid "30514E54-4371-9B2C-2ED9-38BC534924C2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 1.7763568394002365e-015 1.6675544373762092 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.97419780339629847 0.22569590128716774 0
		 0 -0.22569590128716774 0.97419780339629847 0 0 4.6118780223795106 8.1972997175920046 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "L_TeethUpper_Sec_00_Skeleton" -p "TeethUpper_Second_GRP";
	rename -uid "41C6ED5E-481D-4FE9-D870-83BB2EB59341";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.0546792475043478 8.8817841970011182e-016 1.3578020262286945 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 45.000000000000014 0 ;
	setAttr ".bps" -type "matrix" 0.70710678118654746 0.15959110228616599 -0.68886187299856183 0
		 0 0.97419780339629847 0.22569590128716774 0 0.70710678118654768 -0.15959110228616594 0.68886187299856161 0
		 1.2062406368665213 4.7159946563617536 7.7478888264590688 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "L_TeethUpper_Sec_01_Skeleton" -p "TeethUpper_Second_GRP";
	rename -uid "CFA09E17-49EC-2FF5-8354-C9BA2C8D9BEF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6487280759755345 3.5527136788004907e-015 0.49565872128082633 ;
	setAttr ".r" -type "double3" 0 74.008938896552792 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-016 0.22569590128716774 -0.97419780339629847 0
		 0 0.97419780339629847 0.22569590128716774 0 1 -5.0114557234508026e-017 2.1631536637396442e-016 0
		 1.6675544373762092 4.9882382240685503 6.5727718476563508 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "R_TeethUpper_Sec_00_Skeleton" -p "TeethUpper_Second_GRP";
	rename -uid "466DC190-46A8-000E-A829-58BCA318DA23";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.0546792475043478 8.8817841970012523e-016 1.3578020262286952 ;
	setAttr ".r" -type "double3" 5.3413554850939972e-015 90 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 45.000000000000014 0 ;
	setAttr ".bps" -type "matrix" -0.70710678118654746 0.15959110228616596 -0.68886187299856172 0
		 0 0.97419780339629847 0.22569590128716774 0 0.70710678118654757 0.15959110228616594 -0.68886187299856161 0
		 -1.2062406368665213 4.7159946563617536 7.7478888264590697 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "R_TeethUpper_Sec_01_Skeleton" -p "TeethUpper_Second_GRP";
	rename -uid "4C3EE3DF-402C-8437-96A6-C6BB7D8A6ED6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.6487280759755345 3.5527136788005009e-015 0.49565872128082766 ;
	setAttr ".r" -type "double3" 5.0888874903416268e-014 105.99106110344718 2.5444437451708134e-014 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-016 0.22569590128716779 -0.97419780339629869 0
		 0 0.97419780339629847 0.22569590128716774 0 1.0000000000000002 -5.0114557234508026e-017 2.1631536637396442e-016 0
		 -1.6675544373762092 4.9882382240685503 6.5727718476563508 1;
	setAttr ".radi" 0.52142483943309115;
createNode parentConstraint -n "TeethUpper_Second_GRP_parentConstraint1" -p "TeethUpper_Second_GRP";
	rename -uid "6E56F38A-4CE9-1033-A38A-419C4EB51F96";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_TeethUpper_00_SkeletonW0" -dv 1 
		-min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 0 2.2204460492503131e-016 ;
	setAttr ".lr" -type "double3" 13.043803025650517 0 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "TeethUpper_Second_GRP_scaleConstraint1" -p "TeethUpper_Second_GRP";
	rename -uid "B832904E-4228-389F-8BE7-FBB1063BBD2D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_TeethUpper_00_SkeletonW0" -dv 1 
		-min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode joint -n "L_TeethUpper_Sec_02_Skeleton" -p "TeethUpper_Second_GRP";
	rename -uid "B1BAC22E-4865-0C70-AC95-4FBB027F2195";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6675544373762092 1.7763568394002367e-015 -0.46766429718667984 ;
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-016 0.22569590128716774 -0.97419780339629847 0
		 0 0.97419780339629847 0.22569590128716774 0 1 -5.0114557234508026e-017 2.1631536637396442e-016 0
		 1.6675544373762092 5.0937881391219282 6.1171743166102139 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "R_TeethUpper_Sec_02_Skeleton" -p "TeethUpper_Second_GRP";
	rename -uid "74749DBC-4F79-2C31-AEA8-A5BD6B379F6F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.6675544373762092 2.6645352591003757e-015 -0.46766429718667979 ;
	setAttr ".r" -type "double3" -3.373487674796208e-015 89.999999999999986 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-016 0.22569590128716779 -0.97419780339629869 0
		 0 0.97419780339629847 0.22569590128716774 0 1.0000000000000002 -5.0114557234508026e-017 2.1631536637396442e-016 0
		 -1.6675544373762092 5.0937881391219291 6.1171743166102139 1;
	setAttr ".radi" 0.52142483943309115;
createNode transform -n "TeethLower_Second_GRP" -p "HeadLower_None_GRP";
	rename -uid "C8EE0DD9-4A02-81E7-6598-9C8FDC529C52";
	setAttr -l on ".v" no;
createNode joint -n "M_TeethLower_Sec_00_Skeleton" -p "TeethLower_Second_GRP";
	rename -uid "D3D73189-4F8E-CF3D-B7FC-BB976648ED16";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 1.7763568394002365e-015 1.6675544373762092 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.96944136472832787 0.24532313456679325 0
		 0 -0.24532313456679325 0.96944136472832787 0 0 3.4199367585495035 7.9189670716413518 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "L_TeethLower_Sec_00_Skeleton" -p "TeethLower_Second_GRP";
	rename -uid "F37F8CBB-4724-9139-3F5B-488C333DE549";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.0546792475043469 1.7763568394002363e-015 1.335281605874683 ;
	setAttr ".r" -type "double3" 0 -8.3029844037696332 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 45.000000000000014 0 ;
	setAttr ".bps" -type "matrix" 0.70710678118654746 0.17346965203411946 -0.68549856296214196 0
		 0 0.96944136472832787 0.24532313456679325 0 0.70710678118654768 -0.1734696520341194 0.68549856296214173 0
		 1.2062406368665213 3.5331077061094605 7.4717503913072294 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "L_TeethLower_Sec_01_Skeleton" -p "TeethLower_Second_GRP";
	rename -uid "BF5427D2-41F6-C1FC-D118-5D98ED257830";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6675544373762095 1.7763568394002365e-015 0.47331411436026927 ;
	setAttr ".r" -type "double3" 0 70.246217221178895 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-016 0.24532313456679325 -0.96944136472832787 0
		 0 0.96944136472832787 0.24532313456679325 0 1 -5.4472678493853899e-017 2.1525922482908474e-016 0
		 1.6675544373762092 3.8290264401874006 6.3023708221125805 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "R_TeethLower_Sec_00_Skeleton" -p "TeethLower_Second_GRP";
	rename -uid "BEDC5E2B-41FC-A711-F48E-4A8A60B17AB3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.0546792475043469 2.6645352591003757e-015 1.3352816058746821 ;
	setAttr ".r" -type "double3" -5.0888874903416268e-014 98.302984403769628 -5.0888874903416268e-014 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 45.000000000000014 0 ;
	setAttr ".bps" -type "matrix" -0.70710678118654746 0.17346965203411943 -0.68549856296214184 0
		 0 0.96944136472832787 0.24532313456679325 0 0.70710678118654757 0.1734696520341194 -0.68549856296214173 0
		 -1.2062406368665213 3.53310770610946 7.4717503913072303 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "R_TeethLower_Sec_01_Skeleton" -p "TeethLower_Second_GRP";
	rename -uid "5D2AC9A0-4857-1ED5-C579-B9BF733348AF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.6675544373762095 2.6645352591003757e-015 0.47331411436026993 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-014 109.75378277882106 2.5444437451708134e-014 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-016 0.2453231345667933 -0.96944136472832809 0
		 0 0.96944136472832787 0.24532313456679325 0 1.0000000000000002 -5.4472678493853899e-017 2.1525922482908474e-016 0
		 -1.6675544373762092 3.8290264401874006 6.3023708221125805 1;
	setAttr ".radi" 0.52142483943309115;
createNode parentConstraint -n "TeethLower_Second_GRP_parentConstraint1" -p "TeethLower_Second_GRP";
	rename -uid "72AF48E5-49C8-0459-46A0-1E8C9EFA7635";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_TeethLower_00_SkeletonW0" -dv 1 
		-min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -8.8817841970012543e-016 6.6613381477509412e-016 ;
	setAttr ".lr" -type "double3" 14.200930774704792 0 0 ;
	setAttr ".rst" -type "double3" 0 0 9.8607613152626476e-032 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "TeethLower_Second_GRP_scaleConstraint1" -p "TeethLower_Second_GRP";
	rename -uid "29A7E590-4E98-DEA0-4A3C-6190836DB0A2";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_TeethLower_00_SkeletonW0" -dv 1 
		-min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode joint -n "L_TeethLower_Sec_01_Skeleton1" -p "TeethLower_Second_GRP";
	rename -uid "3610445C-4278-DB46-AFE7-75B42189A708";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6675544373762095 3.5527136788004816e-015 -0.48981245749977242 ;
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-016 0.24532313456679325 -0.96944136472832787 0
		 0 0.96944136472832787 0.24532313456679325 0 1 -5.4472678493853899e-017 2.1525922482908474e-016 0
		 1.6675544373762092 3.8290264401874006 6.3023708221125805 1;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "R_TeethLower_Sec_01_Skeleton1" -p "TeethLower_Second_GRP";
	rename -uid "72EEE359-47DF-9226-7D9D-578865D87772";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.6675544373762095 4.4408920985006262e-015 -0.48981245749977287 ;
	setAttr ".r" -type "double3" 4.4979835663949466e-015 89.999999999999972 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-016 0.24532313456679325 -0.96944136472832787 0
		 0 0.96944136472832787 0.24532313456679325 0 1 -5.4472678493853899e-017 2.1525922482908474e-016 0
		 1.6675544373762092 3.8290264401874006 6.3023708221125805 1;
	setAttr ".radi" 0.52142483943309115;
createNode transform -n "HeadMiddle_Skeleton_GRP" -p "M_Head_Skeleton";
	rename -uid "CF0CAC49-48F8-0536-964A-40875912F475";
	setAttr ".t" -type "double3" 0 -6.7213108154266488 0 ;
createNode transform -n "HeadMiddle_None_GRP" -p "HeadMiddle_Skeleton_GRP";
	rename -uid "12A99603-487C-74FF-7E19-07B3A8CF2EB1";
createNode joint -n "M_NoseUpper_Skeleton" -p "HeadMiddle_None_GRP";
	rename -uid "413F0F24-49FA-C9DD-3390-EBB30A8892A4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 7.1184788891751207 9.0628732285632996 ;
	setAttr ".r" -type "double3" 1.9083328088781101e-014 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 9.3132257461547893e-010 122.27111053466797 13.469905853271486 1;
	setAttr ".radi" 0.5;
createNode joint -n "M_Nose_00_Skeleton" -p "M_NoseUpper_Skeleton";
	rename -uid "BD552C2E-4742-27BB-3281-48932C4804D4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 -0.92988739861930014 0.26617513997619469 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.6763806343078613e-008 120.15748596191406 13.428278923034668 1;
	setAttr ".radi" 0.55;
createNode joint -n "M_NoseTip_00_Skeleton" -p "M_Nose_00_Skeleton";
	rename -uid "6B9D9F66-47AD-5284-AE10-F3AA277B6815";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -9.3132257461547852e-010 -0.44022463039973481 0.88738876144773116 ;
	setAttr ".s" -type "double3" 1 1 0.99999999999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 0.99999999999999989 0 -9.3132257461547852e-010 120.9550018310547 14.323205947875977 1;
	setAttr ".radi" 0.55;
createNode joint -n "M_NoseUnder_00_Skeleton" -p "M_Nose_00_Skeleton";
	rename -uid "5D25927D-4C28-3F8A-31EA-45BCD8D5F744";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 -1.2077908618937112 -0.035331937875431763 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.6763806343078613e-008 120.15748596191406 13.428278923034668 1;
	setAttr ".radi" 0.55;
createNode joint -n "L_NoseConner_00_Skeleton" -p "M_Nose_00_Skeleton";
	rename -uid "A98BE2F3-4C42-B630-EEE4-0EA3B47ED481";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.43381721563557352 -0.70232153968912137 0.028608110342341675 ;
	setAttr ".r" -type "double3" -3.1805546814635168e-015 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.87212359905242931 120.66517639160156 13.322959899902344 1;
	setAttr ".radi" 0.55;
createNode joint -n "R_NoseConner_00_Skeleton" -p "M_Nose_00_Skeleton";
	rename -uid "26C7A96F-478F-D08F-5D0C-1499218F5AB8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.43381721563557352 -0.70232153968912137 0.028608110342341675 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.87212359905242931 120.66517639160156 13.322959899902344 1;
	setAttr ".radi" 0.55;
createNode transform -n "Facial_CtrlsSpace_GRP" -p "M_Head_Position";
	rename -uid "5CEC9B9A-4845-9A7A-8C7E-D4BBFD971F59";
	setAttr -l on ".v" no;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "R_Check_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "C78CA925-467E-1D91-83A6-C1A4CC0189FA";
createNode transform -n "R_Cheek_00_Gross_CtrlPosition" -p "R_Check_00_Gross_CtrlPosition_GRP";
	rename -uid "BC928455-4625-CF12-8D10-46BAA2E1DFCB";
createNode nurbsCurve -n "R_Cheek_00_Gross_CtrlPositionShape" -p "R_Cheek_00_Gross_CtrlPosition";
	rename -uid "09EDC85D-44C4-BB65-B74D-E8BFE49F61FF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122549 0.78361162489122371 0
		0 1.1081941875543881 0
		-0.78361162489122416 0.7836116248912246 0
		-1.1081941875543881 0 8.8817841970012523e-016
		-0.7836116248912246 -0.78361162489122371 0
		0 -1.1081941875543881 0
		0.78361162489122371 -0.7836116248912246 0
		1.1081941875543881 -8.8817841970012523e-016 0
		0.78361162489122549 0.78361162489122371 0
		0 1.1081941875543881 0
		-0.78361162489122416 0.7836116248912246 0
		;
createNode parentConstraint -n "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_Check_00_Gross_CtrlPosition_GRP";
	rename -uid "C4113838-4D90-E92C-2924-9DA8C4F78C8B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Cheek_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.4622001647949219 4.5758880849462509 6.0692009925842285 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_Check_00_Gross_CtrlPosition_GRP";
	rename -uid "9D0A5F0E-4D2E-CEEC-A2C1-70B066A973BE";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Cheek_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_Check_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "042D3EAC-4BC1-E25A-C588-CAA14D13C047";
createNode transform -n "L_Cheek_00_Gross_CtrlPosition" -p "L_Check_00_Gross_CtrlPosition_GRP";
	rename -uid "57B69CF7-4135-17D3-C893-B4A6DC9F00AB";
createNode nurbsCurve -n "L_Cheek_00_Gross_CtrlPositionShape" -p "L_Cheek_00_Gross_CtrlPosition";
	rename -uid "41050667-4038-3B17-1EF1-0E95548D6A7A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122504 0.78361162489122393 3.3306690738754696e-016
		-1.2643170607829326e-016 1.1081941875543877 -2.2204460492503131e-016
		-0.78361162489122427 0.78361162489122416 1.1102230246251565e-016
		-1.1081941875543879 3.2112695072372295e-016 4.9303806576313238e-032
		-0.78361162489122449 -0.78361162489122393 0
		-3.3392053635905195e-016 -1.1081941875543881 -2.2204460492503131e-016
		0.78361162489122382 -0.78361162489122449 -2.2204460492503131e-016
		1.1081941875543879 -5.9521325992805871e-016 -1.9721522630525295e-031
		0.78361162489122504 0.78361162489122393 3.3306690738754696e-016
		-1.2643170607829326e-016 1.1081941875543877 -2.2204460492503131e-016
		-0.78361162489122427 0.78361162489122416 1.1102230246251565e-016
		;
createNode parentConstraint -n "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_Check_00_Gross_CtrlPosition_GRP";
	rename -uid "CC6BDEE0-438F-B372-89E9-C9B520DC7A81";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Cheek_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 4.4622001647949219 4.5758880849462509 6.0692009925842285 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_Check_00_Gross_CtrlPosition_GRP";
	rename -uid "DF653511-4B10-1C12-8BFB-D3BB06B3B7B4";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Cheek_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidOuter_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "2EBC6501-4321-7144-C569-7789E6079667";
createNode transform -n "R_LidOuter_00_Gross_CtrlPosition" -p "R_LidOuter_00_Gross_CtrlPosition_GRP";
	rename -uid "091F0AB3-4798-0B47-5B2A-DCA77EB2D423";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.37753912385068578 -0.17787296579449396 0.40676780369759147 ;
	setAttr ".s" -type "double3" 1 1 0.99999999999999989 ;
	setAttr ".rp" -type "double3" 3.5527136788005009e-015 0 -1.7763568394002501e-015 ;
	setAttr ".sp" -type "double3" 3.5527136788005009e-015 0 -1.7763568394002505e-015 ;
	setAttr ".spt" -type "double3" 0 0 3.9443045261050586e-031 ;
createNode nurbsCurve -n "R_LidOuter_00_Gross_CtrlPositionShape" -p "R_LidOuter_00_Gross_CtrlPosition";
	rename -uid "CBC2A1EE-4F8A-96C1-7C05-A29678E6B3DE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 10 0 no 3
		15 0 0 0 1 2 3 4 5 6 7 8 9 10 10 10
		13
		0.23376102843631941 0.069103316529581349 -0.57370668258795021
		0.23376102843631941 0.069103316529581349 -0.57370668258795021
		0.23376102843631941 0.069103316529581349 -0.57370668258795021
		0.23376102843631941 -0.3067450810357748 -0.57370668258795021
		0.23376102843631941 -0.3067450810357748 -0.57370668258795021
		0.23376102843631941 -0.3067450810357748 -0.57370668258795021
		0.88100561225058183 0.069103316529581349 -0.57370668258795376
		0.88100561225058183 0.069103316529581349 -0.57370668258795376
		0.88100561225058183 0.069103316529581349 -0.57370668258795376
		0.23376102843630431 0.44495171409494993 -0.57370668258795021
		0.23376102843630431 0.44495171409494993 -0.57370668258795021
		0.23376102843630431 0.44495171409494993 -0.57370668258795021
		0.23376102843631941 0.069103316529581349 -0.57370668258795021
		;
createNode parentConstraint -n "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidOuter_00_Gross_CtrlPosition_GRP";
	rename -uid "E02FA5D5-4CB1-F94C-B9AD-FCADB88BECE4";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.4987268447875977 9.1129188537597656 7.1400823593139648 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidOuter_00_Gross_CtrlPosition_GRP";
	rename -uid "F675A12A-4360-F38B-E851-4DB8908F89F2";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidInner_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "FB3167EB-4A44-3C5E-6D85-FBA4ADCEB60B";
createNode transform -n "R_LidInner_00_Gross_CtrlPosition" -p "R_LidInner_00_Gross_CtrlPosition_GRP";
	rename -uid "E5BE3FEF-4045-D13E-3147-42B9579F56E2";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" -3.5527136788005009e-015 0 1.7763568394002505e-015 ;
	setAttr ".s" -type "double3" 1 1 0.99999999999999989 ;
	setAttr ".rp" -type "double3" 3.5527136788005009e-015 0 -1.7763568394002501e-015 ;
	setAttr ".sp" -type "double3" 3.5527136788005009e-015 0 -1.7763568394002505e-015 ;
	setAttr ".spt" -type "double3" 0 0 3.9443045261050586e-031 ;
createNode nurbsCurve -n "R_LidInner_00_Gross_CtrlPositionShape" -p "R_LidInner_00_Gross_CtrlPosition";
	rename -uid "C3BC6B0E-4409-1B09-B5E1-DFBE29E52B4A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 10 0 no 3
		15 0 0 0 1 2 3 4 5 6 7 8 9 10 10 10
		13
		0.075784982018418434 -0.033895467794037869 -0.72166481492961687
		0.075784982018418434 -0.033895467794037869 -0.72166481492961687
		0.075784982018418434 -0.033895467794037869 -0.72166481492961687
		0.075784982018418434 -0.40974386535939261 -0.72166481492961687
		0.075784982018418434 -0.40974386535939261 -0.72166481492961687
		0.075784982018418434 -0.40974386535939261 -0.72166481492961687
		-0.57145960179584454 -0.033895467794037869 -0.72166481492961265
		-0.57145960179584454 -0.033895467794037869 -0.72166481492961265
		-0.57145960179584454 -0.033895467794037869 -0.72166481492961265
		0.075784982018433089 0.34195292977133179 -0.72166481492961687
		0.075784982018433089 0.34195292977133179 -0.72166481492961687
		0.075784982018433089 0.34195292977133179 -0.72166481492961687
		0.075784982018418434 -0.033895467794037869 -0.72166481492961687
		;
createNode parentConstraint -n "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidInner_00_Gross_CtrlPosition_GRP";
	rename -uid "06C2A49A-494A-ADD2-80AA-0F9BABC162C9";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidInner_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -1.6553013324737549 8.2814254760742187 7.8856148719787598 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidInner_00_Gross_CtrlPosition_GRP";
	rename -uid "50E04797-41A5-B53D-0F1E-F8B44FABD3DD";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidInner_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketLower_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "88E17695-4DD0-4D20-383B-0A8CEFC2CCA2";
createNode transform -n "R_SocketLower_00_Gross_CtrlPosition" -p "R_SocketLower_00_Gross_CtrlPosition_GRP";
	rename -uid "4FFC961B-4B44-AAE7-23B1-C4BDF072BB3F";
createNode nurbsCurve -n "R_SocketLower_00_Gross_CtrlPositionShape" -p "R_SocketLower_00_Gross_CtrlPosition";
	rename -uid "BD39A015-43D2-E7CC-C1DC-62AEA5489656";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.62262372339318617 0.010051927584386 -0.35195383142542713
		-0.62262372339318617 -0.2192312361656592 -0.35195383142542713
		0.62262372339318794 -0.2192312361656592 -0.35195383142542802
		0.62262372339318794 0.010051927584386 -0.35195383142542802
		-0.62262372339318617 0.010051927584386 -0.35195383142542713
		;
createNode parentConstraint -n "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketLower_00_Gross_CtrlPosition_GRP";
	rename -uid "9EBCE08B-438B-957A-633B-4989A8639202";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketLower_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.2839744577947449 7.4680519104003906 7.6035885810852051 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketLower_00_Gross_CtrlPosition_GRP";
	rename -uid "B3A5C587-4A4B-DB5F-0073-DFBD46EA1D2C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketLower_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketUpper_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "927BA2D3-400B-6D93-D8B8-F995E35C01B5";
createNode transform -n "R_SocketUpper_00_Gross_CtrlPosition" -p "R_SocketUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "D419611D-4E6D-B15E-446B-1583F1A49640";
createNode nurbsCurve -n "R_SocketUpper_00_Gross_CtrlPositionShape" -p "R_SocketUpper_00_Gross_CtrlPosition";
	rename -uid "87C0CCCE-4A33-957A-5B08-80A84163536C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.62262372339318706 0.23545141547183768 -0.42226358249552476
		-0.62262372339318706 0.013916175329258706 -0.42226358249552476
		0.62262372339318706 0.013916175329258706 -0.42226358249552476
		0.62262372339318706 0.23545141547183768 -0.42226358249552476
		-0.62262372339318706 0.23545141547183768 -0.42226358249552476
		;
createNode parentConstraint -n "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "CD2E0E4F-4012-CB67-0E61-9E9813888A90";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketUpper_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.3550353050231934 9.7519245147705078 8.0734004974365234 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "C2C3D168-45A4-4AAB-D8F1-3389FE6DB453";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketUpper_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketLower_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "9E765D2B-49FC-2355-BC00-B6B3C9252E22";
createNode transform -n "L_SocketLower_00_Gross_CtrlPosition" -p "L_SocketLower_00_Gross_CtrlPosition_GRP";
	rename -uid "0900B0E2-4B57-7245-D1BB-728748459CC0";
createNode nurbsCurve -n "L_SocketLower_00_Gross_CtrlPositionShape" -p "L_SocketLower_00_Gross_CtrlPosition";
	rename -uid "12F74217-47CC-21CF-98D8-13BB1F63F820";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.62262372339318639 0.010051927584386292 0.35195383142542708
		-0.62262372339318639 -0.21923123616565948 0.35195383142542708
		0.62262372339318817 -0.21923123616565948 0.35195383142542708
		0.62262372339318817 0.010051927584386292 0.35195383142542708
		-0.62262372339318639 0.010051927584386292 0.35195383142542708
		;
createNode parentConstraint -n "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketLower_00_Gross_CtrlPosition_GRP";
	rename -uid "8BE303B4-4613-D9A9-D620-37A3EAFA0D8A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketLower_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 3.2839744577947449 7.4680519104003906 7.6035885810852051 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketLower_00_Gross_CtrlPosition_GRP";
	rename -uid "2F041910-4842-3F5E-C9CE-DFA3166A6F1F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketLower_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketUpper_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "7384C4E5-4670-9833-289A-A4961EE0AF62";
createNode transform -n "L_SocketUpper_00_Gross_CtrlPosition" -p "L_SocketUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "7103DB6F-4237-5B07-653D-AE95902D0EB2";
createNode nurbsCurve -n "L_SocketUpper_00_Gross_CtrlPositionShape" -p "L_SocketUpper_00_Gross_CtrlPosition";
	rename -uid "675D0384-4E99-B3F5-A5C3-4F83820D4DEE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.62262372339318728 0.23545141547183734 0.4222635824955247
		-0.62262372339318728 0.013916175329259012 0.4222635824955247
		0.62262372339318728 0.013916175329259012 0.4222635824955247
		0.62262372339318728 0.23545141547183734 0.4222635824955247
		-0.62262372339318728 0.23545141547183734 0.4222635824955247
		;
createNode parentConstraint -n "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "76FA3E59-46F5-85E1-5ACE-ABA3F58F1738";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketUpper_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 3.3550353050231934 9.7519245147705078 8.0734004974365234 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "C7A65758-4CFA-63E9-087B-C196E3E2DAC0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketUpper_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidLower_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "A52A5E13-4794-F0EA-E18B-D9B77DAB0A7D";
createNode transform -n "R_LidLower_00_Gross_CtrlPosition" -p "R_LidLower_00_Gross_CtrlPosition_GRP";
	rename -uid "78282341-4120-90E3-BADB-2787C1758C3A";
createNode nurbsCurve -n "R_LidLower_00_Gross_CtrlPositionShape" -p "R_LidLower_00_Gross_CtrlPosition";
	rename -uid "7AA48CB9-4BC5-A468-D107-1B85F387AB0A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.52337289056102954 -0.65354261606275443 -0.58414118956690864
		-4.4408920985006262e-016 -0.74924307654133848 -0.58414118956690864
		-0.5233728905610282 -0.65354261606275443 -0.58414118956690864
		-0.90650843775588674 -0.39208409572752956 -0.58414118956690864
		-1.0467457811220564 -0.034925114913720634 -0.58414118956690864
		-0.90650843775588719 0.024447318870677748 -0.58414118956690864
		-0.52337289056102865 0.024449933455814588 -0.58414118956690864
		-4.4408920985006262e-016 0.024450890460395058 -0.58414118956690864
		0.52337289056102776 0.024449933455814588 -0.58414118956690864
		0.9065084377558863 0.024447318870677748 -0.58414118956690864
		1.0467457811220564 -0.034925114913718858 -0.58414118956690864
		0.90650843775588719 -0.39208409572752867 -0.58414118956690864
		0.52337289056102954 -0.65354261606275443 -0.58414118956690864
		-4.4408920985006262e-016 -0.74924307654133848 -0.58414118956690864
		-0.5233728905610282 -0.65354261606275443 -0.58414118956690864
		;
createNode parentConstraint -n "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidLower_00_Gross_CtrlPosition_GRP";
	rename -uid "A778EADA-41A9-A763-DC4F-5FB3B52823FC";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.3083300590515137 8.4016151428222656 7.9009857177734375 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidLower_00_Gross_CtrlPosition_GRP";
	rename -uid "5E2A4BFF-4367-E917-AA66-45BD34597B70";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidUpper_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "53D07145-4E29-B061-FFD2-F59D040EF64E";
createNode transform -n "R_LidUpper_00_Gross_CtrlPosition" -p "R_LidUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "1C870CD5-40EA-9036-4A7C-35A3A78C4195";
createNode nurbsCurve -n "R_LidUpper_00_Gross_CtrlPositionShape" -p "R_LidUpper_00_Gross_CtrlPosition";
	rename -uid "6C32EAB6-4E9F-843F-7E2E-FBACB379A2DE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.52337289056102954 0.66728377430422192 -0.58414118956690775
		-4.4408920985006262e-016 0.76587360111489922 -0.58414118956690775
		-0.5233728905610282 0.66728377430422192 -0.58414118956690775
		-0.90650843775588719 0.39793135834804438 -0.58414118956690775
		-1.0467457811220569 0.029989115581191328 -0.58414118956690775
		-0.90650843775588763 -0.031175877093446047 -0.58414118956690775
		-0.52337289056102909 -0.031178570617539592 -0.58414118956690775
		-4.4408920985006262e-016 -0.031179556515782636 -0.58414118956690775
		0.52337289056102776 -0.031178570617539592 -0.58414118956690775
		0.9065084377558863 -0.031175877093446047 -0.58414118956690775
		1.0467457811220564 0.029989115581189552 -0.58414118956690775
		0.90650843775588719 0.39793135834804438 -0.58414118956690775
		0.52337289056102954 0.66728377430422192 -0.58414118956690775
		-4.4408920985006262e-016 0.76587360111489922 -0.58414118956690775
		-0.5233728905610282 0.66728377430422192 -0.58414118956690775
		;
createNode parentConstraint -n "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "C1645B1B-41DB-4ADA-A984-37981E4149C0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.3179900646209717 8.7515964508056641 7.9887332916259766 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "53296F1A-481E-76AA-E657-7A869E628B0F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidLower_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "0C98C5F1-4F6F-1861-FA79-459F3470D768";
createNode transform -n "L_LidLower_00_Gross_CtrlPosition" -p "L_LidLower_00_Gross_CtrlPosition_GRP";
	rename -uid "DF194FCF-4535-75D7-35AB-9283279DA6EF";
createNode nurbsCurve -n "L_LidLower_00_Gross_CtrlPositionShape" -p "L_LidLower_00_Gross_CtrlPosition";
	rename -uid "24385F86-4E6B-D1B0-FED6-4AB982D7D6A5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.52337289056102954 -0.65354261606275466 0.58414118956690864
		-2.9672778948456972e-016 -0.74924307654133826 0.5841411895669083
		-0.52337289056102809 -0.65354261606275466 0.58414118956690875
		-0.90650843775588685 -0.3920840957275295 0.58414118956690864
		-1.0467457811220564 -0.034925114913720481 0.58414118956690864
		-0.90650843775588719 0.024447318870677037 0.58414118956690886
		-0.52337289056102876 0.024449933455814553 0.58414118956690864
		-6.6071759651022318e-016 0.024450890460395131 0.58414118956690886
		0.52337289056102776 0.024449933455814397 0.58414118956690864
		0.90650843775588652 0.024447318870676877 0.58414118956690853
		1.0467457811220566 -0.034925114913719447 0.58414118956690875
		0.90650843775588719 -0.39208409572752889 0.58414118956690864
		0.52337289056102954 -0.65354261606275466 0.58414118956690864
		-2.9672778948456972e-016 -0.74924307654133826 0.5841411895669083
		-0.52337289056102809 -0.65354261606275466 0.58414118956690875
		;
createNode parentConstraint -n "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidLower_00_Gross_CtrlPosition_GRP";
	rename -uid "8F5C10C2-4D49-B3B9-BC27-0982A72B4481";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 3.3083300590515137 8.4016151428222656 7.9009857177734375 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidLower_00_Gross_CtrlPosition_GRP";
	rename -uid "43C745A6-4FFF-575B-243E-27A6E6FC7573";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidUpper_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "FA929281-44F9-CA28-9A97-48A331D632AF";
createNode transform -n "L_LidUpper_00_Gross_CtrlPosition" -p "L_LidUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "A0B77425-483F-929A-EAB6-C88B309DBDB9";
createNode nurbsCurve -n "L_LidUpper_00_Gross_CtrlPositionShape" -p "L_LidUpper_00_Gross_CtrlPosition";
	rename -uid "323A78AF-41E9-28F7-10F9-BB80F5D38643";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.52337289056102954 0.66728377430422281 0.58414118956690853
		-2.9672778948456972e-016 0.76587360111489855 0.58414118956690864
		-0.52337289056102809 0.66728377430422281 0.5841411895669083
		-0.90650843775588685 0.39793135834804455 0.58414118956690864
		-1.0467457811220564 0.029989115581190738 0.58414118956690864
		-0.90650843775588719 -0.031175877093446876 0.58414118956690841
		-0.52337289056102876 -0.031178570617538752 0.58414118956690875
		-6.6071759651022318e-016 -0.031179556515781852 0.58414118956690864
		0.52337289056102776 -0.031178570617538752 0.58414118956690853
		0.90650843775588652 -0.031175877093446876 0.58414118956690864
		1.0467457811220566 0.029989115581189624 0.58414118956690853
		0.90650843775588719 0.39793135834804388 0.58414118956690853
		0.52337289056102954 0.66728377430422281 0.58414118956690853
		-2.9672778948456972e-016 0.76587360111489855 0.58414118956690864
		-0.52337289056102809 0.66728377430422281 0.5841411895669083
		;
createNode parentConstraint -n "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "48F77156-491B-60B7-AA5C-E593AA777F51";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 3.3179900646209717 8.7515964508056641 7.9887332916259766 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "2CFFF2F7-4465-F551-587C-5F9342503AFE";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidInner_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "469A67BB-4BE4-0A85-D114-6F9D0C4D629F";
createNode transform -n "L_LidInner_00_Gross_CtrlPosition" -p "L_LidInner_00_Gross_CtrlPosition_GRP";
	rename -uid "541DC5A7-4942-F79B-2495-8DB9FBD2928E";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" -3.5527136788005009e-015 0 1.7763568394002505e-015 ;
	setAttr ".s" -type "double3" 1 1 0.99999999999999989 ;
	setAttr ".rp" -type "double3" 3.5527136788005009e-015 0 -1.7763568394002501e-015 ;
	setAttr ".sp" -type "double3" 3.5527136788005009e-015 0 -1.7763568394002505e-015 ;
	setAttr ".spt" -type "double3" 0 0 3.9443045261050586e-031 ;
createNode nurbsCurve -n "L_LidInner_00_Gross_CtrlPositionShape" -p "L_LidInner_00_Gross_CtrlPosition";
	rename -uid "45317373-4FAF-2BB8-3E6D-3BAFCA41CC58";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 10 0 no 3
		15 0 0 0 1 2 3 4 5 6 7 8 9 10 10 10
		13
		0.075784982018418962 -0.033895467794037792 0.72166481492961265
		0.075784982018418962 -0.033895467794037792 0.72166481492961265
		0.075784982018418962 -0.033895467794037792 0.72166481492961265
		0.075784982018418962 -0.40974386535939283 0.72166481492961265
		0.075784982018418962 -0.40974386535939283 0.72166481492961265
		0.075784982018418962 -0.40974386535939283 0.72166481492961265
		-0.57145960179584387 -0.033895467794037869 0.72166481492960843
		-0.57145960179584387 -0.033895467794037869 0.72166481492960843
		-0.57145960179584387 -0.033895467794037869 0.72166481492960843
		0.075784982018433616 0.3419529297713319 0.72166481492961265
		0.075784982018433616 0.3419529297713319 0.72166481492961265
		0.075784982018433616 0.3419529297713319 0.72166481492961265
		0.075784982018418962 -0.033895467794037792 0.72166481492961265
		;
createNode parentConstraint -n "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidInner_00_Gross_CtrlPosition_GRP";
	rename -uid "6134303D-4F1D-8380-4897-AAB8F9AB9498";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidInner_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 1.6553013324737549 8.2814254760742187 7.8856148719787598 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidInner_00_Gross_CtrlPosition_GRP";
	rename -uid "A258273C-406A-B382-BACF-6186E84D22CE";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidInner_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidOuter_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "AF25D468-4A33-13D8-0333-8BAE6852CC71";
createNode transform -n "L_LidOuter_00_Gross_CtrlPosition" -p "L_LidOuter_00_Gross_CtrlPosition_GRP";
	rename -uid "7909C8C1-4574-CCFD-758D-A39CE96B610D";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" -3.5527136788005009e-015 0 1.7763568394002505e-015 ;
	setAttr ".s" -type "double3" 1 1 0.99999999999999989 ;
	setAttr ".rp" -type "double3" 3.5527136788005009e-015 0 -1.7763568394002501e-015 ;
	setAttr ".sp" -type "double3" 3.5527136788005009e-015 0 -1.7763568394002505e-015 ;
	setAttr ".spt" -type "double3" 0 0 3.9443045261050586e-031 ;
createNode nurbsCurve -n "L_LidOuter_00_Gross_CtrlPositionShape" -p "L_LidOuter_00_Gross_CtrlPosition";
	rename -uid "D73D9A0D-4840-4AE9-8516-ABB79F9F0EE3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 10 0 no 3
		15 0 0 0 1 2 3 4 5 6 7 8 9 10 10 10
		13
		0.23376102843631846 0.069103316529579295 0.57370668258794577
		0.23376102843631846 0.069103316529579295 0.57370668258794577
		0.23376102843631846 0.069103316529579295 0.57370668258794577
		0.23376102843631846 -0.30674508103577575 0.57370668258794577
		0.23376102843631846 -0.30674508103577575 0.57370668258794577
		0.23376102843631846 -0.30674508103577575 0.57370668258794577
		0.88100561225058116 0.069103316529579212 0.57370668258794966
		0.88100561225058116 0.069103316529579212 0.57370668258794966
		0.88100561225058116 0.069103316529579212 0.57370668258794966
		0.23376102843630381 0.44495171409494899 0.57370668258794566
		0.23376102843630381 0.44495171409494899 0.57370668258794566
		0.23376102843630381 0.44495171409494899 0.57370668258794566
		0.23376102843631846 0.069103316529579295 0.57370668258794577
		;
createNode parentConstraint -n "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidOuter_00_Gross_CtrlPosition_GRP";
	rename -uid "40FB232B-4CC5-0D40-B675-BC8E83031FCB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 4.8247900009155273 9.2105464935302734 6.5966176986694336 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidOuter_00_Gross_CtrlPosition_GRP";
	rename -uid "F3D5E38A-46BF-43D6-264A-2FB9603C179B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "M_Nose_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "CAF56300-49BE-163A-EBA9-D08D39B5808D";
createNode transform -n "M_Nose_00_Gross_CtrlPosition" -p "M_Nose_00_Gross_CtrlPosition_GRP";
	rename -uid "22E3FBCC-4A7C-4E89-39B7-57847092C467";
createNode nurbsCurve -n "M_Nose_00_Gross_CtrlPositionShape" -p "M_Nose_00_Gross_CtrlPosition";
	rename -uid "3F103681-424E-BE67-1B6C-97970EBAA0C8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.54667902756795095 0.54085523056186924 0.42653055827504288
		-0.54668090347697373 0.22534899069698894 0.71550636472612095
		-0.54667902756795062 -0.090157249167891362 1.0044821711771981
		-6.9148709946073789e-016 -0.090158331815977072 1.0044831627870741
		0.54667902756795106 -0.090157249167891473 1.0044821711771978
		0.54668090347697385 0.22534899069698849 0.71550636472612128
		0.54667902756795084 0.54085523056186924 0.42653055827504288
		9.1743220972202218e-016 0.54085631320995475 0.42652956666516628
		-0.54667902756795095 0.54085523056186924 0.42653055827504288
		-0.54668090347697373 0.22534899069698894 0.71550636472612095
		-0.54667902756795062 -0.090157249167891362 1.0044821711771981
		;
createNode parentConstraint -n "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "M_Nose_00_Gross_CtrlPosition_GRP";
	rename -uid "57963C81-45D9-728D-1306-818E324DFB42";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_Nose_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 0 6.1885914905558206 9.3290483685394943 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "M_Nose_00_Gross_CtrlPosition_GRP";
	rename -uid "D0F61621-4508-319B-DB75-7A96ED9C66B0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_Nose_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "M_NoseUpper_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "A346ADB6-4AED-7D81-BFB6-8587706882CA";
createNode transform -n "M_NoseUpper_00_Gross_CtrlPosition" -p "M_NoseUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "C9D3302E-44AC-A3D9-C464-E9A6B2A094CF";
createNode nurbsCurve -n "M_NoseUpper_00_Gross_CtrlPositionShape" -p "M_NoseUpper_00_Gross_CtrlPosition";
	rename -uid "C192D85D-4AAE-9899-699D-FEBD8B8B6581";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.49060858353251491 0.5022920059494751 0.15928300923859917
		-0.49061026703786648 0.14636132630241511 0.35459305922987583
		-0.49060858353251424 -0.20956935334464485 0.54990310922115027
		-6.6613381477509392e-016 -0.20957057470771162 0.54990377942041979
		0.49060858353251502 -0.20956935334464494 0.54990310922115027
		0.49061026703786659 0.14636132630241466 0.35459305922987561
		0.49060858353251446 0.5022920059494751 0.15928300923859928
		8.8817841970012523e-016 0.50229322731254167 0.15928233903933028
		-0.49060858353251491 0.5022920059494751 0.15928300923859917
		-0.49061026703786648 0.14636132630241511 0.35459305922987583
		-0.49060858353251424 -0.20956935334464485 0.54990310922115027
		;
createNode parentConstraint -n "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "M_NoseUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "944A48B7-4EB9-2084-2039-F8BBBF30F550";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_NoseUpper_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 0 7.1184788891751207 9.0628732285632996 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "M_NoseUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "8BE5E609-4C72-2A36-3ABA-41982AC1F57C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_NoseUpper_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "M_Mouth_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "9647D0E8-4CB0-E539-D3B5-D0A2903AFB02";
createNode transform -n "M_Mouth_00_Gross_CtrlPosition" -p "M_Mouth_00_Gross_CtrlPosition_GRP";
	rename -uid "349571BC-41EE-7477-95EA-EF8592927352";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 3.5527136788005009e-015 0 ;
	setAttr ".rp" -type "double3" 0 -3.5527136788005009e-015 0 ;
	setAttr ".sp" -type "double3" 0 -3.5527136788005009e-015 0 ;
createNode nurbsCurve -n "M_Mouth_00_Gross_CtrlPositionShape" -p "M_Mouth_00_Gross_CtrlPosition";
	rename -uid "5AB0D793-4A70-758E-631D-619720737C9C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-1.3306494701847793 -1.1267897611541238 -0.4460840087467719
		2.1469344936146388e-016 -1.5667862846225733 -0.28254250539011916
		1.330649470184778 -1.1267897611541238 -0.4460840087467719
		1.881822527499887 -0.84479265502159318 -0.55069341105363745
		1.3306494701847784 -1.6277543220249351 -0.60092715098004312
		5.6702985340686916e-016 -2.1961090122853006 -0.47705987496357116
		-1.3306494701847771 -1.6277543220249351 -0.60092715098004312
		-1.881822527499887 -0.84479265502159318 -0.55069341105363745
		-1.3306494701847793 -1.1267897611541238 -0.4460840087467719
		2.1469344936146388e-016 -1.5667862846225733 -0.28254250539011916
		1.330649470184778 -1.1267897611541238 -0.4460840087467719
		;
createNode parentConstraint -n "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "M_Mouth_00_Gross_CtrlPosition_GRP";
	rename -uid "CF12FC84-4E3C-04A9-C353-FB902A37BF4B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "M_LipLower_00_SkeletonW1" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".rst" -type "double3" 0 3.7628376483917236 8.9172945022583008 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode scaleConstraint -n "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "M_Mouth_00_Gross_CtrlPosition_GRP";
	rename -uid "835164B8-486B-1D50-DAF5-AE90003745D9";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "M_LipLower_00_SkeletonW1" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode transform -n "R_LipConner_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "EFB0B536-4384-C6DD-3B31-5596195AAF6D";
createNode transform -n "R_LipConner_00_Gross_CtrlPosition" -p "R_LipConner_00_Gross_CtrlPosition_GRP";
	rename -uid "7711150B-41CD-82DF-B282-009D6FB82C4C";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 1.7763568394002505e-015 0 1.7763568394002505e-015 ;
	setAttr ".rp" -type "double3" -1.7763568394002505e-015 0 -1.7763568394002505e-015 ;
	setAttr ".sp" -type "double3" -1.7763568394002505e-015 0 -1.7763568394002505e-015 ;
createNode nurbsCurve -n "R_LipConner_00_Gross_CtrlPositionShape" -p "R_LipConner_00_Gross_CtrlPosition";
	rename -uid "A39BE5C2-4521-90FE-37C2-248409987EE0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 10 0 no 3
		15 0 0 0 1 2 3 4 5 6 7 8 9 10 10 10
		13
		-0.19863643277885346 -0.0017623901366761174 -0.71884998493983421
		-0.19863643277885346 -0.0017623901366761174 -0.71884998493983421
		-0.19863643277885346 -0.0017623901366761174 -0.71884998493983421
		-0.19863643277885346 0.48423929008933886 -0.71884998493983421
		-0.19863643277885346 0.48423929008933886 -0.71884998493983421
		-0.19863643277885346 0.48423929008933886 -0.71884998493983421
		0.63830196389534843 -0.0017623901366761174 -0.71884998493982888
		0.63830196389534843 -0.0017623901366761174 -0.71884998493982888
		0.63830196389534843 -0.0017623901366761174 -0.71884998493982888
		-0.19863643277885346 -0.48776407036269109 -0.71884998493983421
		-0.19863643277885346 -0.48776407036269109 -0.71884998493983421
		-0.19863643277885346 -0.48776407036269109 -0.71884998493983421
		-0.19863643277885346 -0.0017623901366761174 -0.71884998493983421
		;
createNode parentConstraint -n "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LipConner_00_Gross_CtrlPosition_GRP";
	rename -uid "E2CE39DE-4A4D-FF2D-844B-B28F2E7DF77D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LipOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -1.6381075382232666 3.789484977722168 7.848480224609375 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LipConner_00_Gross_CtrlPosition_GRP";
	rename -uid "AB323BA3-4820-782E-B102-0A81DD52D302";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LipOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LipConner_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "880FC6E6-40E3-37AA-195E-4A8044E5C67B";
createNode transform -n "L_LipConner_00_Gross_CtrlPosition" -p "L_LipConner_00_Gross_CtrlPosition_GRP";
	rename -uid "4A91D8DB-4F61-77EE-5270-7F8D10B448C5";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 1.7763568394002505e-015 0 1.7763568394002505e-015 ;
	setAttr ".rp" -type "double3" -1.7763568394002505e-015 0 -1.7763568394002505e-015 ;
	setAttr ".sp" -type "double3" -1.7763568394002505e-015 0 -1.7763568394002505e-015 ;
createNode nurbsCurve -n "L_LipConner_00_Gross_CtrlPositionShape" -p "L_LipConner_00_Gross_CtrlPosition";
	rename -uid "3C972B1A-4DFA-01BE-8C5D-0985B3B03F5F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 10 0 no 3
		15 0 0 0 1 2 3 4 5 6 7 8 9 10 10 10
		13
		-0.19863643277885085 -0.0017623901366761174 0.7188499849398291
		-0.19863643277885085 -0.0017623901366761174 0.7188499849398291
		-0.19863643277885085 -0.0017623901366761174 0.7188499849398291
		-0.19863643277885085 0.48423929008933869 0.7188499849398291
		-0.19863643277885085 0.48423929008933869 0.7188499849398291
		-0.19863643277885085 0.48423929008933869 0.7188499849398291
		0.63830196389535088 -0.0017623901366761174 0.71884998493982488
		0.63830196389535088 -0.0017623901366761174 0.71884998493982488
		0.63830196389535088 -0.0017623901366761174 0.71884998493982488
		-0.19863643277885085 -0.4877640703626912 0.7188499849398291
		-0.19863643277885085 -0.4877640703626912 0.7188499849398291
		-0.19863643277885085 -0.4877640703626912 0.7188499849398291
		-0.19863643277885085 -0.0017623901366761174 0.7188499849398291
		;
createNode parentConstraint -n "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LipConner_00_Gross_CtrlPosition_GRP";
	rename -uid "618A50AF-4026-1167-B11C-809377F936E9";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LipOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 1.6381075382232666 3.789484977722168 7.848480224609375 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LipConner_00_Gross_CtrlPosition_GRP";
	rename -uid "F00B4443-463E-F85E-A25B-5382A8DBF04D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LipOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "M_LipLower_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "8775DFA6-4C5A-D734-396A-BAA3F8ACFBF6";
createNode transform -n "M_LipLower_00_Gross_CtrlPosition" -p "M_LipLower_00_Gross_CtrlPosition_GRP";
	rename -uid "A0ECF520-4FD8-4ED1-39EC-B3BD18C787E4";
	setAttr ".ove" yes;
createNode nurbsCurve -n "M_LipLower_00_Gross_CtrlPositionShape" -p "M_LipLower_00_Gross_CtrlPosition";
	rename -uid "0633390D-4827-FC9A-2183-D5B3FCCB1EF3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 9 0 no 3
		14 0 0 0 1 2 3 4 5 6 7 8 9 9 9
		12
		0 -0.13867105584341521 0.3156538586499415
		1.047207870709328 -0.13867105584341521 0.3156538586499415
		1.047207870709328 -0.13867105584341521 0.3156538586499415
		1.047207870709328 -0.13867105584341521 0.3156538586499415
		0.82967638043905201 -0.48164384025070983 0.31565385864994161
		0.55311758695936808 -0.48164384025070983 0.31565385864994161
		-0.55311758695936808 -0.48164384025070983 0.31565385864994161
		-0.82967638043905201 -0.48164384025070983 0.31565385864994161
		-1.047207870709328 -0.13867105584341521 0.3156538586499415
		-1.047207870709328 -0.13867105584341521 0.3156538586499415
		-1.047207870709328 -0.13867105584341521 0.3156538586499415
		0 -0.13867105584341521 0.3156538586499415
		;
createNode parentConstraint -n "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "M_LipLower_00_Gross_CtrlPosition_GRP";
	rename -uid "6A4CD1C8-4B46-F922-D607-CBA76549F46D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipLower_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 0 3.4986839294433594 8.8420066833496094 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "M_LipLower_00_Gross_CtrlPosition_GRP";
	rename -uid "8E964B8E-49C8-2925-0C3F-7E91CFC0210D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipLower_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "M_LipUpper_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "518919B5-454D-720B-1E8B-8398845C0DB0";
createNode transform -n "M_LipUpper_00_Gross_CtrlPosition" -p "M_LipUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "FFE331E3-4BCE-6FBE-3384-10B269289FE1";
	setAttr ".ove" yes;
createNode nurbsCurve -n "M_LipUpper_00_Gross_CtrlPositionShape" -p "M_LipUpper_00_Gross_CtrlPosition";
	rename -uid "7E34246B-4FBA-7661-D320-AB81E151C063";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 9 0 no 3
		14 0 0 0 1 2 3 4 5 6 7 8 9 9 9
		12
		0 0.14754535033230726 0.31565385864994155
		1.047207870709328 0.14754535033230726 0.31565385864994155
		1.047207870709328 0.14754535033230726 0.31565385864994155
		1.047207870709328 0.14754535033230726 0.31565385864994155
		0.82967638043905201 0.49051813473960149 0.31565385864994155
		0.55311758695936808 0.49051813473960149 0.31565385864994155
		-0.55311758695936808 0.49051813473960149 0.31565385864994155
		-0.82967638043905201 0.49051813473960149 0.31565385864994155
		-1.047207870709328 0.14754535033230726 0.31565385864994155
		-1.047207870709328 0.14754535033230726 0.31565385864994155
		-1.047207870709328 0.14754535033230726 0.31565385864994155
		0 0.14754535033230726 0.31565385864994155
		;
createNode parentConstraint -n "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "M_LipUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "23F8AAAB-405C-DBD0-5B3E-EF9E7EE88E83";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 0 4.0269913673400879 8.9925823211669922 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "M_LipUpper_00_Gross_CtrlPosition_GRP";
	rename -uid "8DD92DED-4EFF-3D02-AE66-7E930487593B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_BrowOuter_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "675FC4CB-48F9-DA7D-9398-1FBFD97304BD";
createNode transform -n "R_BrowOuter_00_Part_CtrlPosition" -p "R_BrowOuter_00_Part_CtrlPosition_GRP";
	rename -uid "780C480B-41A7-86B1-181F-BBAA9875C49C";
	setAttr ".t" -type "double3" 0 -1.7763568394002505e-015 0 ;
createNode nurbsCurve -n "R_BrowOuter_00_Part_CtrlPositionShape" -p "R_BrowOuter_00_Part_CtrlPosition";
	rename -uid "ED5A0637-4E56-B782-301B-22A37EBDDD6F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.44766659585071267 -0.41727145618493644 -0.25671356916520072
		-0.032843473769625042 -0.4172728880366332 -0.30184942557203343
		0.38197964831146081 -0.41727145618493644 -0.34698528197886613
		0.38198107176178286 -2.8421709430404007e-014 -0.34698543686090044
		0.38197964831146081 0.41727145618488848 -0.34698528197886613
		-0.032843473769625042 0.41727288803657636 -0.30184942557203343
		-0.44766659585071267 0.41727145618488848 -0.25671356916520072
		-0.44766801930103473 -2.8421709430404007e-014 -0.25671341428316374
		-0.44766659585071267 -0.41727145618493644 -0.25671356916520072
		-0.032843473769625042 -0.4172728880366332 -0.30184942557203343
		0.38197964831146081 -0.41727145618493644 -0.34698528197886613
		;
createNode parentConstraint -n "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_BrowOuter_00_Part_CtrlPosition_GRP";
	rename -uid "CEEE1FD0-4D37-C893-4A5C-F5B8D0F05DFC";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Brow_03_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -5.8503628894613122 10.3752855238635 5.9211162469652514 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_BrowOuter_00_Part_CtrlPosition_GRP";
	rename -uid "195AF04A-4C5A-DCDC-8B7E-5E91725CDBEE";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Brow_03_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_BrowMiddle_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "B86C0717-4B14-D1A0-D326-4890B8DBAB82";
createNode transform -n "R_BrowMiddle_00_Part_CtrlPosition" -p "R_BrowMiddle_00_Part_CtrlPosition_GRP";
	rename -uid "445349DB-4783-1360-AEB6-398DC8D1DF6F";
	setAttr ".t" -type "double3" 8.8817841970012523e-016 -1.7763568394002505e-015 0 ;
createNode nurbsCurve -n "R_BrowMiddle_00_Part_CtrlPositionShape" -p "R_BrowMiddle_00_Part_CtrlPosition";
	rename -uid "0E94EFE6-4796-DE35-2697-C7AB35EA1A02";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.44766659585071222 -0.41727145618493644 -0.2567135691652016
		-0.032843473769624598 -0.4172728880366332 -0.30184942557203343
		0.38197964831146169 -0.41727145618493644 -0.34698528197886702
		0.38198107176178375 -2.8421709430404007e-014 -0.34698543686090133
		0.38197964831146169 0.41727145618488848 -0.34698528197886702
		-0.032843473769624598 0.41727288803657636 -0.30184942557203343
		-0.44766659585071222 0.41727145618488848 -0.2567135691652016
		-0.44766801930103384 -2.8421709430404007e-014 -0.25671341428316374
		-0.44766659585071222 -0.41727145618493644 -0.2567135691652016
		-0.032843473769624598 -0.4172728880366332 -0.30184942557203343
		0.38197964831146169 -0.41727145618493644 -0.34698528197886702
		;
createNode parentConstraint -n "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_BrowMiddle_00_Part_CtrlPosition_GRP";
	rename -uid "942440B3-4727-72EA-296E-7A949DB046F7";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Brow_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.7354907989501953 10.53758430480957 7.5964393615722656 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_BrowMiddle_00_Part_CtrlPosition_GRP";
	rename -uid "D4296B1F-4FD5-91FB-604D-B5B1DEA564CA";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Brow_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_BrowInner_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "EB205A2F-4610-747B-8DD6-CA9C8F42214C";
createNode transform -n "R_BrowInner_00_Part_CtrlPosition" -p "R_BrowInner_00_Part_CtrlPosition_GRP";
	rename -uid "2D4BB6E8-4E63-B979-059E-5DBBA3C7E223";
	setAttr ".t" -type "double3" 1.1102230246251565e-016 0 0 ;
createNode nurbsCurve -n "R_BrowInner_00_Part_CtrlPositionShape" -p "R_BrowInner_00_Part_CtrlPosition";
	rename -uid "2D7C8444-4794-FB65-FBE6-3F9D27A96027";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.44766659585071222 -0.41727145618493466 -0.25671356916520338
		-0.032843473769625042 -0.41727288803663143 -0.3018494255720352
		0.38197964831146147 -0.41727145618493466 -0.34698528197886702
		0.38198107176178331 -2.6645352591003757e-014 -0.34698543686090311
		0.38197964831146147 0.41727145618489025 -0.34698528197886702
		-0.032843473769625042 0.41727288803657814 -0.3018494255720352
		-0.447666595850712 0.41727145618489025 -0.25671356916520338
		-0.44766801930103362 -2.6645352591003757e-014 -0.25671341428316552
		-0.44766659585071222 -0.41727145618493466 -0.25671356916520338
		-0.032843473769625042 -0.41727288803663143 -0.3018494255720352
		0.38197964831146147 -0.41727145618493466 -0.34698528197886702
		;
createNode parentConstraint -n "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_BrowInner_00_Part_CtrlPosition_GRP";
	rename -uid "9471DBD1-412E-16F5-EEC1-11896D9C39B0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Brow_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -1.4691572189331055 10.356332568764975 9.0161819458007812 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_BrowInner_00_Part_CtrlPosition_GRP";
	rename -uid "D9E0AC64-4111-03F0-5FFE-9A9AEC165A4E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Brow_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_BrowOuter_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "EE1B33C8-490C-4C55-B66A-A5993A51DF41";
createNode transform -n "L_BrowOuter_00_Part_CtrlPosition" -p "L_BrowOuter_00_Part_CtrlPosition_GRP";
	rename -uid "55B5292F-4E62-DE21-DCA4-339AE32A8D75";
	setAttr ".t" -type "double3" 0 1.7763568394002505e-015 0 ;
createNode nurbsCurve -n "L_BrowOuter_00_Part_CtrlPositionShape" -p "L_BrowOuter_00_Part_CtrlPosition";
	rename -uid "86CC7916-44B6-13FC-A9D9-229876F0924C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.44766659585071217 -0.41727145618493472 0.25671356916520149
		-0.032843473769625008 -0.41727288803663148 0.30184942557203387
		0.3819796483114612 -0.41727145618493472 0.34698528197886613
		0.38198107176178331 -2.6645352591003763e-014 0.34698543686090155
		0.38197964831146136 0.41727145618489042 0.34698528197886619
		-0.032843473769625008 0.41727288803657814 0.30184942557203387
		-0.44766659585071206 0.41727145618489042 0.25671356916520155
		-0.44766801930103362 -2.6645352591003763e-014 0.25671341428316513
		-0.44766659585071217 -0.41727145618493472 0.25671356916520149
		-0.032843473769625008 -0.41727288803663148 0.30184942557203387
		0.3819796483114612 -0.41727145618493472 0.34698528197886613
		;
createNode parentConstraint -n "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_BrowOuter_00_Part_CtrlPosition_GRP";
	rename -uid "5AAF8394-4845-7C58-4FD5-E38C83B80E49";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Brow_03_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 5.8503628894613122 10.3752855238635 5.9211162469652514 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_BrowOuter_00_Part_CtrlPosition_GRP";
	rename -uid "7D4711E2-4BB4-B8AC-C6CE-549ABBC8DF02";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Brow_03_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_BrowMiddle_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "510DC0EE-4F0C-BA76-C27B-399D6E6E6595";
createNode transform -n "L_BrowMiddle_00_Part_CtrlPosition" -p "L_BrowMiddle_00_Part_CtrlPosition_GRP";
	rename -uid "F9ECC692-4AEC-DB8A-6C87-CD889503BCA8";
	setAttr ".t" -type "double3" 0 1.7763568394002505e-015 0 ;
createNode nurbsCurve -n "L_BrowMiddle_00_Part_CtrlPositionShape" -p "L_BrowMiddle_00_Part_CtrlPosition";
	rename -uid "6D87404C-46FF-4D37-2592-7ABE3E15435E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.44766659585071217 -0.41727145618493472 0.25671356916520149
		-0.032843473769625008 -0.41727288803663148 0.30184942557203387
		0.3819796483114612 -0.41727145618493472 0.34698528197886613
		0.38198107176178331 -2.6645352591003763e-014 0.34698543686090155
		0.38197964831146136 0.41727145618489042 0.34698528197886619
		-0.032843473769625008 0.41727288803657814 0.30184942557203387
		-0.44766659585071206 0.41727145618489042 0.25671356916520155
		-0.44766801930103362 -2.6645352591003763e-014 0.25671341428316513
		-0.44766659585071217 -0.41727145618493472 0.25671356916520149
		-0.032843473769625008 -0.41727288803663148 0.30184942557203387
		0.3819796483114612 -0.41727145618493472 0.34698528197886613
		;
createNode parentConstraint -n "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_BrowMiddle_00_Part_CtrlPosition_GRP";
	rename -uid "D777ECA7-4B71-DD69-17BD-CC9E05B34E10";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Brow_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 4.7354907989501953 10.53758430480957 7.5964393615722656 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_BrowMiddle_00_Part_CtrlPosition_GRP";
	rename -uid "7957AB74-4DB7-524F-7B08-E78C9037FC69";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Brow_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_BrowInner_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "EFBA5FA0-49FC-B0DD-3D06-FD84F5EF7455";
createNode transform -n "L_BrowInner_00_Part_CtrlPosition" -p "L_BrowInner_00_Part_CtrlPosition_GRP";
	rename -uid "DA36D940-4811-1E85-5FA9-448E3B79D573";
createNode nurbsCurve -n "L_BrowInner_00_Part_CtrlPositionShape" -p "L_BrowInner_00_Part_CtrlPosition";
	rename -uid "6788FB64-460E-8FAB-F608-9C92A6BD1221";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.44766659585071217 -0.41727145618493533 0.25671356916520149
		-0.032843473769625008 -0.41727288803663209 0.30184942557203387
		0.3819796483114612 -0.41727145618493533 0.34698528197886613
		0.38198107176178331 -2.7284841053187852e-014 0.34698543686090155
		0.38197964831146136 0.41727145618488981 0.34698528197886619
		-0.032843473769625008 0.41727288803657753 0.30184942557203387
		-0.44766659585071206 0.41727145618488981 0.25671356916520155
		-0.44766801930103362 -2.7284841053187852e-014 0.25671341428316513
		-0.44766659585071217 -0.41727145618493533 0.25671356916520149
		-0.032843473769625008 -0.41727288803663209 0.30184942557203387
		0.3819796483114612 -0.41727145618493533 0.34698528197886613
		;
createNode parentConstraint -n "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_BrowInner_00_Part_CtrlPosition_GRP";
	rename -uid "7BCA6450-45A9-0D86-BACD-47B1DD235B72";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Brow_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 1.4691572189331055 10.356332568764975 9.0161819458007812 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_BrowInner_00_Part_CtrlPosition_GRP";
	rename -uid "188DE2B5-4630-652C-1C08-958467D93F00";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Brow_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_Brow_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "6B6A6BF7-4E56-5CFF-2A96-AD9CCA93E901";
createNode transform -n "R_Brow_00_Gross_CtrlPosition" -p "R_Brow_00_Gross_CtrlPosition_GRP";
	rename -uid "2317F383-4D3F-DF11-DE33-19A9E1B7EA98";
	setAttr ".ove" yes;
createNode nurbsCurve -n "R_Brow_00_Gross_CtrlPositionShape" -p "R_Brow_00_Gross_CtrlPosition";
	rename -uid "7A60D9DA-45A0-2C3A-CEB1-C587D0C2E9BA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 1.8999999999999999 1.95 2 3 4 5 6 7 8 9 10 11 11.050000000000001 11.100000000000001
		 11.150000000000002 12.150000000000002 13.150000000000002
		15
		-1.7973375392327013 0.34695945198632039 -0.81318192235146647
		-1.8841170777121248 0.63881067898438104 -0.79807429109139072
		-1.89175972253969 0.68693831380771719 -0.80863457994245103
		-1.7664088201157131 0.6868840332799877 -0.80323927860416156
		1.1964152721046597 0.92894348834623663 -0.19070534919377735
		1.1964152721046597 0.92894348834621709 -0.19070534919377735
		2.4909925073383246 0.52515477787806475 0.8131819223514789
		2.4909925073383246 0.52515477787805054 0.81318192235147446
		0.9788512267340419 0.63989463178736727 -0.19070534920022197
		0.97885122673402769 0.63989463178735306 -0.19070534920022197
		-1.703831559093586 0.3365811505994678 -0.8101445708028745
		-1.7584320377527094 0.33599215154027995 -0.80543864416015509
		-1.7973375392327013 0.34695945198632039 -0.81318192235146647
		-1.8841170777121248 0.63881067898438104 -0.79807429109139072
		-1.89175972253969 0.68693831380771719 -0.80863457994245103
		;
createNode parentConstraint -n "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_Brow_00_Gross_CtrlPosition_GRP";
	rename -uid "01A5BE20-4A30-5FC9-6C0D-0FB79E90688D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Brow_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.2037782669067383 10.572027206420898 8.592747688293457 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_Brow_00_Gross_CtrlPosition_GRP";
	rename -uid "22130582-4308-7280-EF82-618EB1DF1433";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Brow_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_Brow_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "21DFDCB2-48A3-246E-5B12-04A228CA3C0E";
createNode transform -n "L_Brow_00_Gross_CtrlPosition" -p "L_Brow_00_Gross_CtrlPosition_GRP";
	rename -uid "3F00BC89-40ED-DED1-A2F0-B0A296461901";
	setAttr ".ove" yes;
createNode nurbsCurve -n "L_Brow_00_Gross_CtrlPositionShape" -p "L_Brow_00_Gross_CtrlPosition";
	rename -uid "25C8305D-4E53-3F0F-4EF3-2DA92C557CF8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 1.8999999999999999 1.95 2 3 4 5 6 7 8 9 10 11 11.050000000000001 11.100000000000001
		 11.150000000000002 12.150000000000002 13.150000000000002
		15
		-1.7973375392327011 0.34695945198632061 0.8131819223514668
		-1.8841170777121246 0.63881067898438049 0.79807429109139039
		-1.8917597225396898 0.68693831380771675 0.80863457994245158
		-1.7664088201157129 0.68688403327998859 0.80323927860416133
		1.1964152721046599 0.92894348834623708 0.19070534919377741
		1.1964152721046599 0.92894348834621698 0.19070534919377741
		2.4909925073383246 0.52515477787806442 -0.81318192235147957
		2.4909925073383246 0.5251547778780512 -0.81318192235147524
		0.97885122673404157 0.63989463178736794 0.19070534920022189
		0.97885122673402769 0.63989463178735384 0.19070534920022189
		-1.7038315590935857 0.33658115059946714 0.81014457080287416
		-1.7584320377527092 0.33599215154027956 0.80543864416015598
		-1.7973375392327011 0.34695945198632061 0.8131819223514668
		-1.8841170777121246 0.63881067898438049 0.79807429109139039
		-1.8917597225396898 0.68693831380771675 0.80863457994245158
		;
createNode parentConstraint -n "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_Brow_00_Gross_CtrlPosition_GRP";
	rename -uid "3FE117EC-48D0-266F-B05F-18AF297A3340";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Brow_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 3.2037782669067383 10.572027206420898 8.592747688293457 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_Brow_00_Gross_CtrlPosition_GRP";
	rename -uid "9AB48E47-4EC0-B275-3465-85B469F0F073";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Brow_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_Orbit_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "9A03C3E1-4540-07A3-C043-6F8DFD0DE35D";
createNode transform -n "R_Orbit_00_Gross_CtrlPosition" -p "R_Orbit_00_Gross_CtrlPosition_GRP";
	rename -uid "45AB7C13-4FF8-FD59-A02A-0EB0B5E4292D";
createNode nurbsCurve -n "R_Orbit_00_Gross_CtrlPositionShape" -p "R_Orbit_00_Gross_CtrlPosition";
	rename -uid "A8736FB2-4D81-8D71-44BD-87A086975656";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122504 0.78361162489122393 3.3306690738754696e-016
		-1.2643170607829326e-016 1.1081941875543877 -2.2204460492503131e-016
		-0.78361162489122427 0.78361162489122416 1.1102230246251565e-016
		-1.1081941875543879 3.2112695072372295e-016 4.9303806576313238e-032
		-0.78361162489122449 -0.78361162489122393 0
		-3.3392053635905195e-016 -1.1081941875543881 -2.2204460492503131e-016
		0.78361162489122382 -0.78361162489122449 -2.2204460492503131e-016
		1.1081941875543879 -5.9521325992805871e-016 -1.9721522630525295e-031
		0.78361162489122504 0.78361162489122393 3.3306690738754696e-016
		-1.2643170607829326e-016 1.1081941875543877 -2.2204460492503131e-016
		-0.78361162489122427 0.78361162489122416 1.1102230246251565e-016
		;
createNode parentConstraint -n "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "R_Orbit_00_Gross_CtrlPosition_GRP";
	rename -uid "A0D218CF-40E1-9944-2741-BDBB4DD835C6";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Orbit_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.4723429679870605 6.6044464111328125 6.7346591949462891 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_Orbit_00_Gross_CtrlPosition_GRP";
	rename -uid "0A7A60CD-4986-2420-144F-64BE05A3AE5A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_Orbit_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_Orbit_00_Gross_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "E7A90C3C-4911-B87C-FDA6-259799A00AB0";
createNode transform -n "L_Orbit_00_Gross_CtrlPosition" -p "L_Orbit_00_Gross_CtrlPosition_GRP";
	rename -uid "49C773F1-44AE-A2F9-3D50-4AB0D499408C";
createNode nurbsCurve -n "L_Orbit_00_Gross_CtrlPositionShape" -p "L_Orbit_00_Gross_CtrlPosition";
	rename -uid "C31FA869-43DD-BE5C-34CB-C387DBC9FEDD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122504 0.78361162489122393 3.3306690738754696e-016
		-1.2643170607829326e-016 1.1081941875543877 -2.2204460492503131e-016
		-0.78361162489122427 0.78361162489122416 1.1102230246251565e-016
		-1.1081941875543879 3.2112695072372295e-016 4.9303806576313238e-032
		-0.78361162489122449 -0.78361162489122393 0
		-3.3392053635905195e-016 -1.1081941875543881 -2.2204460492503131e-016
		0.78361162489122382 -0.78361162489122449 -2.2204460492503131e-016
		1.1081941875543879 -5.9521325992805871e-016 -1.9721522630525295e-031
		0.78361162489122504 0.78361162489122393 3.3306690738754696e-016
		-1.2643170607829326e-016 1.1081941875543877 -2.2204460492503131e-016
		-0.78361162489122427 0.78361162489122416 1.1102230246251565e-016
		;
createNode parentConstraint -n "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1" 
		-p "L_Orbit_00_Gross_CtrlPosition_GRP";
	rename -uid "B558043F-46C1-4724-BD63-A4AB3DF52476";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Orbit_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 4.4723429679870605 6.6044464111328125 6.7346591949462891 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_Orbit_00_Gross_CtrlPosition_GRP";
	rename -uid "0B0D4F62-4AE0-4D59-C625-CFAA30EA7DDE";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_Orbit_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "M_LipUpper_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "B213CC76-4F85-FA0A-ACD9-5FAEE136EEB9";
createNode transform -n "M_LipUpper_00_Part_CtrlPosition" -p "M_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "3EF1010A-495D-60AB-04E9-85A932CAE743";
createNode nurbsCurve -n "M_LipUpper_00_Part_CtrlPositionShape" -p "M_LipUpper_00_Part_CtrlPosition";
	rename -uid "7B5FA609-46D1-E083-E1B8-FFB171121148";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		-0.18130168755117737 0.10467457811220574 0.15581651645427996
		-0.2093491562244113 6.8850506977772091e-017 0.15581651645427996
		-0.18130168755117745 -0.10467457811220565 0.15581651645427996
		-0.10467457811220576 -0.18130168755117729 0.15581651645427996
		-1.3214351930204464e-016 -0.20934915622441133 0.15581651645427996
		0.10467457811220555 -0.18130168755117743 0.15581651645427996
		0.18130168755117732 -0.1046745781122058 0.15581651645427996
		0.20934915622441133 -1.9739203423999582e-016 0.15581651645427996
		0.18130168755117745 0.10467457811220554 0.15581651645427996
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		;
createNode parentConstraint -n "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "M_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "7873236B-4C69-1D91-EB67-C18A38A2411A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -8.8817841970012523e-016 0 ;
	setAttr ".rst" -type "double3" 0 4.026991367340087 8.9925823211669922 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "M_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "4F431982-4EB6-E12D-934C-87B45BDD88C7";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LipUpper_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "074EB152-4C35-998C-86DF-AEA19834F3CD";
createNode transform -n "L_LipUpper_00_Part_CtrlPosition" -p "L_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "5ABAB141-494D-F322-DEE8-0689E1F84CAD";
createNode nurbsCurve -n "L_LipUpper_00_Part_CtrlPositionShape" -p "L_LipUpper_00_Part_CtrlPosition";
	rename -uid "1F285B97-478C-3575-9078-C3A260F6AC49";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		-0.18130168755117737 0.10467457811220574 0.15581651645427996
		-0.2093491562244113 6.8850506977772091e-017 0.15581651645427996
		-0.18130168755117745 -0.10467457811220565 0.15581651645427996
		-0.10467457811220576 -0.18130168755117729 0.15581651645427996
		-1.3214351930204464e-016 -0.20934915622441133 0.15581651645427996
		0.10467457811220555 -0.18130168755117743 0.15581651645427996
		0.18130168755117732 -0.1046745781122058 0.15581651645427996
		0.20934915622441133 -1.9739203423999582e-016 0.15581651645427996
		0.18130168755117745 0.10467457811220554 0.15581651645427996
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		;
createNode parentConstraint -n "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "3865C743-4660-BCC1-9E8E-06A792E2206F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LipUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -2.2204460492503131e-016 -2.6645352591003757e-015 
		0 ;
	setAttr ".rst" -type "double3" 1.0074524879455564 4.0015859603881809 8.5875701904296875 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "7269BF28-438F-12A3-ACDA-1C9DE7485B60";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LipUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LipLower_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "363B296A-49AC-EFB8-A065-A18D58733D85";
createNode transform -n "L_LipLower_00_Part_CtrlPosition" -p "L_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "0D601A04-4B95-B231-8C90-BFA43FEA01A8";
createNode nurbsCurve -n "L_LipLower_00_Part_CtrlPositionShape" -p "L_LipLower_00_Part_CtrlPosition";
	rename -uid "13A282D5-4DA1-19FC-DA6B-FE8B7C2E3614";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		-0.18130168755117737 0.10467457811220574 0.15581651645427996
		-0.2093491562244113 6.8850506977772091e-017 0.15581651645427996
		-0.18130168755117745 -0.10467457811220565 0.15581651645427996
		-0.10467457811220576 -0.18130168755117729 0.15581651645427996
		-1.3214351930204464e-016 -0.20934915622441133 0.15581651645427996
		0.10467457811220555 -0.18130168755117743 0.15581651645427996
		0.18130168755117732 -0.1046745781122058 0.15581651645427996
		0.20934915622441133 -1.9739203423999582e-016 0.15581651645427996
		0.18130168755117745 0.10467457811220554 0.15581651645427996
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		;
createNode parentConstraint -n "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "C2A1923A-46FE-2BA3-8014-7B8839DA1D9A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LipLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 1.0965092182159424 3.5773906707763672 8.4012517929077148 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "FC9F891A-4020-08BA-462D-DB8735033723";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LipLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "M_LipLower_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "DB4CC098-4D70-410E-2455-A9AA86FBE799";
createNode transform -n "M_LipLower_00_Part_CtrlPosition" -p "M_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "2C4CD22D-4F11-6683-B414-CB9591215AE1";
createNode nurbsCurve -n "M_LipLower_00_Part_CtrlPositionShape" -p "M_LipLower_00_Part_CtrlPosition";
	rename -uid "43DBC84A-471D-A9C6-9E9C-C684B25DF685";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		-0.18130168755117737 0.10467457811220574 0.15581651645427996
		-0.2093491562244113 6.8850506977772091e-017 0.15581651645427996
		-0.18130168755117745 -0.10467457811220565 0.15581651645427996
		-0.10467457811220576 -0.18130168755117729 0.15581651645427996
		-1.3214351930204464e-016 -0.20934915622441133 0.15581651645427996
		0.10467457811220555 -0.18130168755117743 0.15581651645427996
		0.18130168755117732 -0.1046745781122058 0.15581651645427996
		0.20934915622441133 -1.9739203423999582e-016 0.15581651645427996
		0.18130168755117745 0.10467457811220554 0.15581651645427996
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		;
createNode parentConstraint -n "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "M_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "73A6C8F9-46EF-4F54-6D0A-8D88126E7021";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipLower_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 0 3.4986839294433594 8.8420066833496094 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "M_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "60707E55-4E85-3C44-8A2E-48BCD2F77830";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "M_LipLower_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LipUpper_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "A49C456D-4C3D-1153-DE9F-A1A02420416A";
createNode transform -n "R_LipUpper_00_Part_CtrlPosition" -p "R_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "7C987095-4E92-BF36-64A3-69B0F6B6A50E";
createNode nurbsCurve -n "R_LipUpper_00_Part_CtrlPositionShape" -p "R_LipUpper_00_Part_CtrlPosition";
	rename -uid "EB134639-4121-036E-D29E-0FA4154AA693";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.10467457811220604 0.18130168755117726 -0.15581651645427996
		2.2204460492503131e-016 0.20934915622441164 -0.15581651645427996
		-0.10467457811220537 0.18130168755117726 -0.15581651645427996
		-0.18130168755117715 0.10467457811220537 -0.15581651645427996
		-0.20934915622441108 0 -0.15581651645427996
		-0.18130168755117726 -0.10467457811220582 -0.15581651645427996
		-0.1046745781122056 -0.18130168755117726 -0.15581651645427996
		0 -0.20934915622441119 -0.15581651645427996
		0.10467457811220582 -0.18130168755117726 -0.15581651645427996
		0.18130168755117748 -0.10467457811220582 -0.15581651645427996
		0.20934915622441164 0 -0.15581651645427996
		0.1813016875511777 0.10467457811220537 -0.15581651645427996
		0.10467457811220604 0.18130168755117726 -0.15581651645427996
		2.2204460492503131e-016 0.20934915622441164 -0.15581651645427996
		-0.10467457811220537 0.18130168755117726 -0.15581651645427996
		;
createNode parentConstraint -n "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "5F8C753F-494F-A5D3-53EE-CCB22C836017";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LipUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -4.4408920985006262e-016 -2.6645352591003757e-015 
		0 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -1.0074524879455562 4.0015859603881809 8.5875701904296875 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LipUpper_00_Part_CtrlPosition_GRP";
	rename -uid "E417A8F5-48E2-C0EC-4044-F1B1780DAA5F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LipUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LipLower_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "88935D7E-42F5-8C33-6DAC-A18FC3130121";
createNode transform -n "R_LipLower_00_Part_CtrlPosition" -p "R_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "E17E2582-4E6B-746E-15ED-D39FCB95B17D";
createNode nurbsCurve -n "R_LipLower_00_Part_CtrlPositionShape" -p "R_LipLower_00_Part_CtrlPosition";
	rename -uid "0BB8F0B6-424A-94A4-EFA7-608640491B87";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.10467457811220582 0.18130168755117726 -0.15581651645427996
		0 0.20934915622441119 -0.15581651645427996
		-0.10467457811220549 0.18130168755117726 -0.15581651645427996
		-0.18130168755117726 0.10467457811220582 -0.15581651645427996
		-0.20934915622441119 0 -0.15581651645427996
		-0.18130168755117737 -0.10467457811220582 -0.15581651645427996
		-0.10467457811220571 -0.18130168755117726 -0.15581651645427996
		-2.2204460492503131e-016 -0.20934915622441119 -0.15581651645427996
		0.1046745781122056 -0.18130168755117726 -0.15581651645427996
		0.18130168755117726 -0.10467457811220582 -0.15581651645427996
		0.20934915622441141 0 -0.15581651645427996
		0.18130168755117748 0.10467457811220537 -0.15581651645427996
		0.10467457811220582 0.18130168755117726 -0.15581651645427996
		0 0.20934915622441119 -0.15581651645427996
		-0.10467457811220549 0.18130168755117726 -0.15581651645427996
		;
createNode parentConstraint -n "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "4F263ACB-41F3-C0FF-F8BA-629AC05C4517";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LipLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -1.0965092182159424 3.5773906707763672 8.4012517929077148 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LipLower_00_Part_CtrlPosition_GRP";
	rename -uid "4A0F40DD-40D1-3AA8-3310-B38AB8EFB024";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LipLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LipConner_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "91A13C95-447B-231A-C76B-2288231919B5";
createNode transform -n "L_LipConner_00_Part_CtrlPosition" -p "L_LipConner_00_Part_CtrlPosition_GRP";
	rename -uid "2773FC07-4DDF-25D8-D59D-69928EC0669D";
createNode nurbsCurve -n "L_LipConner_00_Part_CtrlPositionShape" -p "L_LipConner_00_Part_CtrlPosition";
	rename -uid "743E886E-48E6-9384-106E-939D479AEA70";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		-0.18130168755117737 0.10467457811220574 0.15581651645427996
		-0.2093491562244113 6.8850506977772091e-017 0.15581651645427996
		-0.18130168755117745 -0.10467457811220565 0.15581651645427996
		-0.10467457811220576 -0.18130168755117729 0.15581651645427996
		-1.3214351930204464e-016 -0.20934915622441133 0.15581651645427996
		0.10467457811220555 -0.18130168755117743 0.15581651645427996
		0.18130168755117732 -0.1046745781122058 0.15581651645427996
		0.20934915622441133 -1.9739203423999582e-016 0.15581651645427996
		0.18130168755117745 0.10467457811220554 0.15581651645427996
		0.10467457811220592 0.1813016875511772 0.15581651645427996
		-5.9345557896913951e-017 0.20934915622441139 0.15581651645427996
		-0.10467457811220562 0.18130168755117734 0.15581651645427996
		;
createNode parentConstraint -n "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LipConner_00_Part_CtrlPosition_GRP";
	rename -uid "E4ACD844-4083-F6BB-8DB6-BBB2904DE21F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LipOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 2.2204460492503131e-016 8.8817841970012523e-016 
		1.7763568394002505e-015 ;
	setAttr ".rst" -type "double3" 1.6381075382232668 3.7894849777221689 7.8484802246093768 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LipConner_00_Part_CtrlPosition_GRP";
	rename -uid "DA6E6E4F-4BAF-43A5-8BAF-439AB71512C5";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LipOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LipConner_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "91E291D9-4852-8070-83A5-7692FB3627CF";
createNode transform -n "R_LipConner_00_Part_CtrlPosition" -p "R_LipConner_00_Part_CtrlPosition_GRP";
	rename -uid "E9670DD0-43A2-8D6E-CD61-91A37F7D88F7";
createNode nurbsCurve -n "R_LipConner_00_Part_CtrlPositionShape" -p "R_LipConner_00_Part_CtrlPosition";
	rename -uid "0A612376-4AFA-1080-611D-E28CD9B43534";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.10467457811220582 0.18130168755117726 -0.15581651645427996
		0 0.20934915622441119 -0.15581651645427996
		-0.1046745781122056 0.18130168755117726 -0.15581651645427996
		-0.18130168755117748 0.10467457811220582 -0.15581651645427996
		-0.20934915622441141 0 -0.15581651645427996
		-0.18130168755117748 -0.10467457811220582 -0.15581651645427996
		-0.10467457811220582 -0.18130168755117726 -0.15581651645427996
		-2.2204460492503131e-016 -0.20934915622441119 -0.15581651645427996
		0.1046745781122056 -0.18130168755117726 -0.15581651645427996
		0.18130168755117726 -0.10467457811220582 -0.15581651645427996
		0.20934915622441141 0 -0.15581651645427996
		0.18130168755117748 0.10467457811220537 -0.15581651645427996
		0.10467457811220582 0.18130168755117726 -0.15581651645427996
		0 0.20934915622441119 -0.15581651645427996
		-0.1046745781122056 0.18130168755117726 -0.15581651645427996
		;
createNode parentConstraint -n "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LipConner_00_Part_CtrlPosition_GRP";
	rename -uid "7156C37E-469F-E6B3-487A-C8A4CF3A61C5";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LipOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 2.2204460492503131e-016 8.8817841970012523e-016 
		-1.7763568394002505e-015 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -1.6381075382232668 3.7894849777221689 7.8484802246093768 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LipConner_00_Part_CtrlPosition_GRP";
	rename -uid "2FC133D2-43D8-7BCB-A5A9-F7A3613BEDDB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LipOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidUpper_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "795EC12C-4252-D8D1-5F4C-64B38406E848";
createNode transform -n "L_LidUpper_00_Part_CtrlPosition" -p "L_LidUpper_00_Part_CtrlPosition_GRP";
	rename -uid "7397E22F-49EC-B20D-CB3D-53BF5583C76B";
createNode nurbsCurve -n "L_LidUpper_00_Part_CtrlPositionShape" -p "L_LidUpper_00_Part_CtrlPosition";
	rename -uid "A37AC0A7-4A9E-0774-0F16-53BF0966029D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830887 0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 0.31402373433661707 0.23372477468141994
		-0.15701186716830845 0.271952531326766 0.23372477468141994
		-0.27195253132676606 0.15701186716830862 0.23372477468141994
		-0.31402373433661696 1.0327576046665814e-016 0.23372477468141994
		-0.27195253132676617 -0.016921620569736257 0.23372477468141994
		-0.15701186716830864 -0.016922769976348812 0.23372477468141994
		-1.9821527895306695e-016 -0.016923190688368284 0.23372477468141994
		0.15701186716830834 -0.016922769976348812 0.23372477468141994
		0.271952531326766 -0.016921620569736257 0.23372477468141994
		0.31402373433661701 -2.9608805135999374e-016 0.23372477468141994
		0.27195253132676617 0.15701186716830831 0.23372477468141994
		0.15701186716830887 0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 0.31402373433661707 0.23372477468141994
		-0.15701186716830845 0.271952531326766 0.23372477468141994
		;
createNode parentConstraint -n "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidUpper_00_Part_CtrlPosition_GRP";
	rename -uid "E43015D3-43BD-1574-50DA-7C8711290EFB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 2.0917415618896484 8.615190713301752 8.0394248962402344 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidUpper_00_Part_CtrlPosition_GRP";
	rename -uid "DE45767D-4A48-30F1-27F3-7082C61D3C82";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidUpper_01_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "E60781F8-4DCC-2F7C-FB4F-57AFCDDA475A";
createNode transform -n "L_LidUpper_01_Part_CtrlPosition" -p "L_LidUpper_01_Part_CtrlPosition_GRP";
	rename -uid "B953AC0F-43CF-B490-BE1E-AFAF16BAC48A";
createNode nurbsCurve -n "L_LidUpper_01_Part_CtrlPositionShape" -p "L_LidUpper_01_Part_CtrlPosition";
	rename -uid "5E5EFF52-4ABA-DCCC-3491-23BFDCBBCD81";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830887 0.27195253132676578 0.23372477468142039
		-8.901833684537092e-017 0.31402373433661707 0.23372477468142039
		-0.15701186716830845 0.271952531326766 0.23372477468142039
		-0.27195253132676606 0.15701186716830862 0.23372477468142039
		-0.31402373433661696 1.0327576046665814e-016 0.23372477468142039
		-0.27195253132676617 -0.016921620569736257 0.23372477468142039
		-0.15701186716830864 -0.016922769976348812 0.23372477468142039
		-1.9821527895306695e-016 -0.016923190688368284 0.23372477468142039
		0.15701186716830834 -0.016922769976348812 0.23372477468142039
		0.271952531326766 -0.016921620569736257 0.23372477468142039
		0.31402373433661701 -2.9608805135999374e-016 0.23372477468142039
		0.27195253132676617 0.15701186716830831 0.23372477468142039
		0.15701186716830887 0.27195253132676578 0.23372477468142039
		-8.901833684537092e-017 0.31402373433661707 0.23372477468142039
		-0.15701186716830845 0.271952531326766 0.23372477468142039
		;
createNode parentConstraint -n "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidUpper_01_Part_CtrlPosition_GRP";
	rename -uid "A8445164-434F-65F0-A0A9-CC8A87FEEBAF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 4.4408920985006262e-016 0 0 ;
	setAttr ".rst" -type "double3" 3.3179900646209721 8.615190713301752 7.9887332916259766 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidUpper_01_Part_CtrlPosition_GRP";
	rename -uid "F371A923-4491-08BB-B0F3-59916D8433D8";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidUpper_02_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "E50DD2B5-4DE1-ABFA-2025-1EAA8642E723";
createNode transform -n "L_LidUpper_02_Part_CtrlPosition" -p "L_LidUpper_02_Part_CtrlPosition_GRP";
	rename -uid "12E4D2B3-45B2-D5B1-1721-BAA4FFFEB290";
createNode nurbsCurve -n "L_LidUpper_02_Part_CtrlPositionShape" -p "L_LidUpper_02_Part_CtrlPosition";
	rename -uid "7F89F070-4293-C3A0-63D3-A6BD093A9BCC";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830887 0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 0.31402373433661707 0.23372477468141994
		-0.15701186716830845 0.271952531326766 0.23372477468141994
		-0.27195253132676606 0.15701186716830862 0.23372477468141994
		-0.31402373433661696 1.0327576046665814e-016 0.23372477468141994
		-0.27195253132676617 -0.016921620569736257 0.23372477468141994
		-0.15701186716830864 -0.016922769976348812 0.23372477468141994
		-1.9821527895306695e-016 -0.016923190688368284 0.23372477468141994
		0.15701186716830834 -0.016922769976348812 0.23372477468141994
		0.271952531326766 -0.016921620569736257 0.23372477468141994
		0.31402373433661701 -2.9608805135999374e-016 0.23372477468141994
		0.27195253132676617 0.15701186716830831 0.23372477468141994
		0.15701186716830887 0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 0.31402373433661707 0.23372477468141994
		-0.15701186716830845 0.271952531326766 0.23372477468141994
		;
createNode parentConstraint -n "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidUpper_02_Part_CtrlPosition_GRP";
	rename -uid "5BA97BA6-460A-418B-6A58-C69CA1FB3EFB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidUpper_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 0 8.8817841970012523e-016 ;
	setAttr ".rst" -type "double3" 4.4987268447875977 8.615190713301752 7.2066859685625957 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidUpper_02_Part_CtrlPosition_GRP";
	rename -uid "5EBBA356-4386-E79B-0024-BA9EAF8838B8";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidUpper_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidLower_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "020BF9F3-4DB6-C81D-2814-E99B5E90FCAE";
createNode transform -n "L_LidLower_00_Part_CtrlPosition" -p "L_LidLower_00_Part_CtrlPosition_GRP";
	rename -uid "70CF22F7-4C53-0F09-68A3-9F81CE6B52A5";
createNode nurbsCurve -n "L_LidLower_00_Part_CtrlPositionShape" -p "L_LidLower_00_Part_CtrlPosition";
	rename -uid "291C9924-4748-6677-A70D-A5AC80B5A60A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830887 -0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 -0.31402373433661707 0.23372477468141994
		-0.15701186716830845 -0.271952531326766 0.23372477468141994
		-0.27195253132676606 -0.15701186716830862 0.23372477468141994
		-0.31402373433661696 -1.0327576046665814e-016 0.23372477468141994
		-0.27195253132676617 0.016921620569736257 0.23372477468141994
		-0.15701186716830864 0.016922769976348812 0.23372477468141994
		-1.9821527895306695e-016 0.016923190688368284 0.23372477468141994
		0.15701186716830834 0.016922769976348812 0.23372477468141994
		0.271952531326766 0.016921620569736257 0.23372477468141994
		0.31402373433661701 2.9608805135999374e-016 0.23372477468141994
		0.27195253132676617 -0.15701186716830831 0.23372477468141994
		0.15701186716830887 -0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 -0.31402373433661707 0.23372477468141994
		-0.15701186716830845 -0.271952531326766 0.23372477468141994
		;
createNode parentConstraint -n "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidLower_00_Part_CtrlPosition_GRP";
	rename -uid "C26361D0-4647-6F1B-ACED-97AF196638F4";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidLower_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 2.0934193134307861 8.2652094053183536 7.9774303436279297 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidLower_00_Part_CtrlPosition_GRP";
	rename -uid "3D564493-40C2-8DBC-4E05-49B5B36FCA01";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidLower_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidLower_01_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "AC6C9964-4989-A6AA-C7D6-7E94676FD10B";
createNode transform -n "L_LidLower_01_Part_CtrlPosition" -p "L_LidLower_01_Part_CtrlPosition_GRP";
	rename -uid "943DE87B-4B7E-0EC7-9AAE-0BAB6ABC6B31";
createNode nurbsCurve -n "L_LidLower_01_Part_CtrlPositionShape" -p "L_LidLower_01_Part_CtrlPosition";
	rename -uid "DBB01783-4F2F-B664-4B45-9BA0C3D4E5D6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830887 -0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 -0.31402373433661707 0.23372477468141994
		-0.15701186716830845 -0.271952531326766 0.23372477468141994
		-0.27195253132676606 -0.15701186716830862 0.23372477468141994
		-0.31402373433661696 -1.0327576046665814e-016 0.23372477468141994
		-0.27195253132676617 0.016921620569736257 0.23372477468141994
		-0.15701186716830864 0.016922769976348812 0.23372477468141994
		-1.9821527895306695e-016 0.016923190688368284 0.23372477468141994
		0.15701186716830834 0.016922769976348812 0.23372477468141994
		0.271952531326766 0.016921620569736257 0.23372477468141994
		0.31402373433661701 2.9608805135999374e-016 0.23372477468141994
		0.27195253132676617 -0.15701186716830831 0.23372477468141994
		0.15701186716830887 -0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 -0.31402373433661707 0.23372477468141994
		-0.15701186716830845 -0.271952531326766 0.23372477468141994
		;
createNode parentConstraint -n "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidLower_01_Part_CtrlPosition_GRP";
	rename -uid "F238CF03-4FE3-1216-8CAE-12A6A82351A3";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -8.8817841970012523e-016 -1.7763568394002505e-015 
		8.8817841970012523e-016 ;
	setAttr ".rst" -type "double3" 3.3083300590515128 8.2652094053183518 7.9009857177734384 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidLower_01_Part_CtrlPosition_GRP";
	rename -uid "17453AFD-43F5-285B-83CB-49A74D7965A3";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidLower_02_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "B4B65DB8-480F-C6B3-766B-AE9C9E1DC322";
createNode transform -n "L_LidLower_02_Part_CtrlPosition" -p "L_LidLower_02_Part_CtrlPosition_GRP";
	rename -uid "9A08B541-440F-8813-5BA7-E9AB4F92765F";
createNode nurbsCurve -n "L_LidLower_02_Part_CtrlPositionShape" -p "L_LidLower_02_Part_CtrlPosition";
	rename -uid "BD025211-492A-74D8-218D-D5A029CFAFF1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830887 -0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 -0.31402373433661707 0.23372477468141994
		-0.15701186716830845 -0.271952531326766 0.23372477468141994
		-0.27195253132676606 -0.15701186716830862 0.23372477468141994
		-0.31402373433661696 -1.0327576046665814e-016 0.23372477468141994
		-0.27195253132676617 0.016921620569736257 0.23372477468141994
		-0.15701186716830864 0.016922769976348812 0.23372477468141994
		-1.9821527895306695e-016 0.016923190688368284 0.23372477468141994
		0.15701186716830834 0.016922769976348812 0.23372477468141994
		0.271952531326766 0.016921620569736257 0.23372477468141994
		0.31402373433661701 2.9608805135999374e-016 0.23372477468141994
		0.27195253132676617 -0.15701186716830831 0.23372477468141994
		0.15701186716830887 -0.27195253132676578 0.23372477468141994
		-8.901833684537092e-017 -0.31402373433661707 0.23372477468141994
		-0.15701186716830845 -0.271952531326766 0.23372477468141994
		;
createNode parentConstraint -n "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidLower_02_Part_CtrlPosition_GRP";
	rename -uid "C9EB7FBB-4558-85DC-C4CA-65ABBBF73DE1";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidLower_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -8.8817841970012523e-016 0 -8.8817841970012523e-016 ;
	setAttr ".rst" -type "double3" 4.4987268447875968 8.2652094053183536 7.1507586919512658 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidLower_02_Part_CtrlPosition_GRP";
	rename -uid "BD9B7669-4C8A-415A-86EF-C2AF3130F6FB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidLower_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketUpper_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "955F9C40-4586-ED8C-3777-679200802768";
createNode transform -n "L_SocketUpper_00_Part_CtrlPosition" -p "L_SocketUpper_00_Part_CtrlPosition_GRP";
	rename -uid "21E36705-45F8-44A0-BB84-CA8E16FACC9E";
createNode nurbsCurve -n "L_SocketUpper_00_Part_CtrlPositionShape" -p "L_SocketUpper_00_Part_CtrlPosition";
	rename -uid "B27B5905-4B0F-3C9E-D289-E5B8E32C1ACA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		;
createNode parentConstraint -n "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketUpper_00_Part_CtrlPosition_GRP";
	rename -uid "CAD40D01-43DC-A25E-F79F-12AC359BCACB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketUpper_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -1.7763568394002505e-015 0 ;
	setAttr ".rst" -type "double3" 2.0917415618896484 9.1716892260193692 8.280426025390625 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketUpper_00_Part_CtrlPosition_GRP";
	rename -uid "660F049D-46B0-66EA-3993-43A9A173AFEB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketUpper_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketUpper_01_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "4811D23B-443B-30C1-A29B-1AB857661699";
createNode transform -n "L_SocketUpper_01_Part_CtrlPosition" -p "L_SocketUpper_01_Part_CtrlPosition_GRP";
	rename -uid "99577328-48AC-2E3D-70B8-279666D9F313";
createNode nurbsCurve -n "L_SocketUpper_01_Part_CtrlPositionShape" -p "L_SocketUpper_01_Part_CtrlPosition";
	rename -uid "19D89C6B-4893-EF5B-89C6-418E76B8DB7E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		;
createNode parentConstraint -n "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketUpper_01_Part_CtrlPosition_GRP";
	rename -uid "0E6E01B6-4A97-DD39-3534-D68EED02EA9B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketUpper_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -1.7763568394002505e-015 0 ;
	setAttr ".rst" -type "double3" 3.3179900646209717 9.1716892260193692 8.0734004974365234 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketUpper_01_Part_CtrlPosition_GRP";
	rename -uid "D89B2660-466E-CFAD-389C-F4B1B79DCF95";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketUpper_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketUpper_02_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "FCBFA6C4-4852-D94D-A795-6B84B733F583";
createNode transform -n "L_SocketUpper_02_Part_CtrlPosition" -p "L_SocketUpper_02_Part_CtrlPosition_GRP";
	rename -uid "761FBCE0-4CA2-0F5E-5845-3BAF7A2C4FBF";
createNode nurbsCurve -n "L_SocketUpper_02_Part_CtrlPositionShape" -p "L_SocketUpper_02_Part_CtrlPosition";
	rename -uid "1E4EA4E2-4367-D8FF-C57C-1D98C9DEAE1D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		;
createNode parentConstraint -n "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketUpper_02_Part_CtrlPosition_GRP";
	rename -uid "ABA5265F-4E52-42F4-7759-ECB0B2175765";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketUpper_02_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -1.7763568394002505e-015 8.8817841970012523e-016 ;
	setAttr ".rst" -type "double3" 4.4987268447875977 9.1716892260193692 7.3598788098301391 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketUpper_02_Part_CtrlPosition_GRP";
	rename -uid "6592F16A-42D9-EA1E-A0C6-9AB43F63BEDA";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketUpper_02_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketLower_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "A01F3DCF-4E90-FA06-8CCD-69BB04B37D22";
createNode transform -n "L_SocketLower_00_Part_CtrlPosition" -p "L_SocketLower_00_Part_CtrlPosition_GRP";
	rename -uid "83C7D1BC-4A60-2FD2-1017-5E8CCFD7E032";
createNode nurbsCurve -n "L_SocketLower_00_Part_CtrlPositionShape" -p "L_SocketLower_00_Part_CtrlPosition";
	rename -uid "6C9540BD-432A-85D1-E16C-F3BDFD3A5CDD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		;
createNode parentConstraint -n "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketLower_00_Part_CtrlPosition_GRP";
	rename -uid "927FB644-44EF-DF31-F989-D785DAD69A46";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketLower_02_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 4.4987268447875977 7.71017785963177 7.0099451855625601 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketLower_00_Part_CtrlPosition_GRP";
	rename -uid "11CE4FD0-4740-4B6A-E7B3-F2980B396985";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketLower_02_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketLower_01_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "27E64F46-47AC-C419-F019-31A05EE3345C";
createNode transform -n "L_SocketLower_01_Part_CtrlPosition" -p "L_SocketLower_01_Part_CtrlPosition_GRP";
	rename -uid "040B1ACC-4DF8-F289-18ED-16B2CD8696E2";
	setAttr ".t" -type "double3" 1.3322676295501878e-015 1.7763568394002505e-015 1.7763568394002505e-015 ;
createNode nurbsCurve -n "L_SocketLower_01_Part_CtrlPositionShape" -p "L_SocketLower_01_Part_CtrlPosition";
	rename -uid "29F16B4E-412C-A9D4-A94C-06B737D55AD6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		;
createNode parentConstraint -n "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketLower_01_Part_CtrlPosition_GRP";
	rename -uid "73A1C1E3-4BDC-17E9-25C2-BB835E5F51C4";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketLower_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 4.4408920985006262e-016 0 8.8817841970012523e-016 ;
	setAttr ".rst" -type "double3" 3.3083300590515141 7.71017785963177 7.603588581085206 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketLower_01_Part_CtrlPosition_GRP";
	rename -uid "9E5D2CF5-4A26-D3C8-814D-24B7139183AA";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketLower_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketLower_02_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "33FE5661-46F7-ACBE-3B9E-F7B7B56B9205";
createNode transform -n "L_SocketLower_02_Part_CtrlPosition" -p "L_SocketLower_02_Part_CtrlPosition_GRP";
	rename -uid "84493971-40D8-08FC-5D62-7BAE07774394";
createNode nurbsCurve -n "L_SocketLower_02_Part_CtrlPositionShape" -p "L_SocketLower_02_Part_CtrlPosition";
	rename -uid "E62B6F51-458D-80D7-EB28-8AB24A5C41D1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 -0.11466059452736146 0.31669768687164351
		0.25335102051838915 0.11466059452736146 0.31669768687164351
		-0.25335102051838915 0.11466059452736146 0.31669768687164351
		;
createNode parentConstraint -n "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketLower_02_Part_CtrlPosition_GRP";
	rename -uid "75D2DE04-4E29-A2F3-D17A-A885E089F89D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketLower_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 2.0934193134307861 7.71017785963177 7.840672492980957 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketLower_02_Part_CtrlPosition_GRP";
	rename -uid "4B33D4EC-46CB-D311-A77C-4AA07E490B2C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketLower_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidInner_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "4C74C6EA-406D-C793-2B81-16B49FF195E1";
createNode transform -n "L_LidInner_00_Part_CtrlPosition" -p "L_LidInner_00_Part_CtrlPosition_GRP";
	rename -uid "696735E0-4BE5-41AB-2D36-D28E54A1EC47";
createNode nurbsCurve -n "L_LidInner_00_Part_CtrlPositionShape" -p "L_LidInner_00_Part_CtrlPosition";
	rename -uid "7609786C-4C35-F7D9-F9C1-CAADDD1FF21D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		-0.29033203672200714 0.15701186716831103 0.17155172947280345
		-0.33240323973185837 1.9567680809018384e-015 0.17155172947280345
		-0.29033203672200736 -0.15701186716830631 0.17155172947280345
		-0.17539137256354997 -0.271952531326764 0.17155172947280345
		-0.018379505395241504 -0.3140237343366149 0.17155172947280345
		-0.0014578848255051013 -0.27195253132676411 0.17155172947280345
		-0.0014567354188925671 -0.15701186716830656 0.17155172947280345
		-0.001456314706873095 1.8943180357666733e-015 0.17155172947280345
		-0.001456735418892588 0.15701186716831042 0.17155172947280345
		-0.0014578848255050597 0.27195253132676805 0.17155172947280345
		-0.018379505395241108 0.31402373433661912 0.17155172947280345
		-0.17539137256354967 0.27195253132676833 0.17155172947280345
		-0.29033203672200714 0.15701186716831103 0.17155172947280345
		-0.33240323973185837 1.9567680809018384e-015 0.17155172947280345
		-0.29033203672200736 -0.15701186716830631 0.17155172947280345
		;
createNode parentConstraint -n "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidInner_00_Part_CtrlPosition_GRP";
	rename -uid "5CFB7C1A-4106-A7C6-9C3E-93944F741041";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidInner_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -1.7763568394002505e-015 0 ;
	setAttr ".rst" -type "double3" 1.6553013324737549 8.4373177475072563 7.8856148719787598 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidInner_00_Part_CtrlPosition_GRP";
	rename -uid "D740440F-4391-C865-4844-03BA6318BEA6";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidInner_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_LidOuter_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "F913CC8F-416C-150C-4989-60ABB52FADE5";
createNode transform -n "L_LidOuter_00_Part_CtrlPosition" -p "L_LidOuter_00_Part_CtrlPosition_GRP";
	rename -uid "87FC2C4E-43A5-067E-0C33-BBBF9011B10E";
createNode nurbsCurve -n "L_LidOuter_00_Part_CtrlPositionShape" -p "L_LidOuter_00_Part_CtrlPosition";
	rename -uid "7A78D9EF-4E0A-C2C4-8001-3DBE8658EB77";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.29589458670431018 -0.15701186716831095 0.17155172947280345
		0.33796578971416147 -1.85268467234323e-015 0.17155172947280345
		0.29589458670431051 0.15701186716830637 0.17155172947280345
		0.18095392254585319 0.271952531326764 0.17155172947280345
		0.023942055377544541 0.31402373433661512 0.17155172947280345
		0.007020434807808118 0.27195253132676422 0.17155172947280345
		0.007019285401195563 0.1570118671683067 0.17155172947280345
		0.0070188646891761741 -1.6861512186494565e-015 0.17155172947280345
		0.0070192854011957295 -0.15701186716831025 0.17155172947280345
		0.007020434807808118 -0.27195253132676783 0.17155172947280345
		0.023942055377544041 -0.31402373433661901 0.17155172947280345
		0.18095392254585269 -0.27195253132676822 0.17155172947280345
		0.29589458670431018 -0.15701186716831095 0.17155172947280345
		0.33796578971416147 -1.85268467234323e-015 0.17155172947280345
		0.29589458670431051 0.15701186716830637 0.17155172947280345
		;
createNode parentConstraint -n "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_LidOuter_00_Part_CtrlPosition_GRP";
	rename -uid "7614A0F8-4492-F507-D876-70A0DB1A2216";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 4.876265968638287 8.437317747507258 6.7999181648650051 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_LidOuter_00_Part_CtrlPosition_GRP";
	rename -uid "87AD2282-4D4A-ED37-1BE4-CA82F102448C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_LidOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketInner_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "48B7F828-4EBE-1966-5C5A-A699EAA4737C";
createNode transform -n "L_SocketInner_00_Part_CtrlPosition" -p "L_SocketInner_00_Part_CtrlPosition_GRP";
	rename -uid "9FCD8E30-4837-DC1A-6555-ECB5D8E19ACC";
createNode nurbsCurve -n "L_SocketInner_00_Part_CtrlPositionShape" -p "L_SocketInner_00_Part_CtrlPosition";
	rename -uid "A6B4693F-4CF6-7AB7-4194-E7ADECDFDE6C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.1146605945273614 -0.25335102051838909 0.31669768687164351
		0.11466059452736148 -0.2533510205183892 0.31669768687164351
		0.1146605945273614 0.25335102051838909 0.31669768687164351
		-0.11466059452736148 0.2533510205183892 0.31669768687164351
		-0.1146605945273614 -0.25335102051838909 0.31669768687164351
		;
createNode parentConstraint -n "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketInner_00_Part_CtrlPosition_GRP";
	rename -uid "F2771DF2-4FC9-ABBF-FC5E-EE9B638FFD42";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketInner_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -4.4408920985006262e-016 -5.3290705182007514e-015 
		0 ;
	setAttr ".rst" -type "double3" 1.2401901235847819 8.442024174684418 8.0583465244996688 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketInner_00_Part_CtrlPosition_GRP";
	rename -uid "290CC05E-4E00-F5D2-FD43-B88047442EA2";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketInner_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "L_SocketOuter_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "842E0CB5-463E-64E5-7288-AA9A46075438";
createNode transform -n "L_SocketOuter_00_Part_CtrlPosition" -p "L_SocketOuter_00_Part_CtrlPosition_GRP";
	rename -uid "9752B272-468C-47CB-DEE3-B28B2AA9C639";
createNode nurbsCurve -n "L_SocketOuter_00_Part_CtrlPositionShape" -p "L_SocketOuter_00_Part_CtrlPosition";
	rename -uid "C57A4147-4EAB-776E-CE56-429633F47A8A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.1146605945273614 -0.25335102051838909 0.31669768687164351
		0.11466059452736148 -0.2533510205183892 0.31669768687164351
		0.1146605945273614 0.25335102051838909 0.31669768687164351
		-0.11466059452736148 0.2533510205183892 0.31669768687164351
		-0.1146605945273614 -0.25335102051838909 0.31669768687164351
		;
createNode parentConstraint -n "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "L_SocketOuter_00_Part_CtrlPosition_GRP";
	rename -uid "1C280775-4281-13BB-2AC1-10ABB55BB556";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketOuter_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 5.2656780232713203 8.437317747507258 6.3903667231273822 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "L_SocketOuter_00_Part_CtrlPosition_GRP";
	rename -uid "CB857F0F-4118-D6C1-6557-B1BD2C100C13";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "L_SocketOuter_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidUpper_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "A1B74D8E-422C-E782-39C8-BC8A4C985AA9";
createNode transform -n "R_LidUpper_00_Part_CtrlPosition" -p "R_LidUpper_00_Part_CtrlPosition_GRP";
	rename -uid "820D07A8-4AE0-BED1-B84B-5A9E83E643F3";
createNode nurbsCurve -n "R_LidUpper_00_Part_CtrlPositionShape" -p "R_LidUpper_00_Part_CtrlPosition";
	rename -uid "47AF9CA4-4416-0BDF-13AD-5FA1D0BDC77C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830873 0.27195253132676456 -0.23372477468141994
		0 0.31402373433661612 -0.23372477468141994
		-0.15701186716830873 0.27195253132676722 -0.23372477468141994
		-0.27195253132676622 0.15701186716830939 -0.23372477468141994
		-0.31402373433661712 0 -0.23372477468141994
		-0.27195253132676656 -0.016921620569736007 -0.23372477468141994
		-0.15701186716830906 -0.016922769976348562 -0.23372477468141994
		0 -0.01692319068836845 -0.23372477468141994
		0.15701186716830806 -0.016922769976348562 -0.23372477468141994
		0.27195253132676589 -0.016921620569736007 -0.23372477468141994
		0.31402373433661679 0 -0.23372477468141994
		0.27195253132676589 0.15701186716830939 -0.23372477468141994
		0.15701186716830873 0.27195253132676456 -0.23372477468141994
		0 0.31402373433661612 -0.23372477468141994
		-0.15701186716830873 0.27195253132676722 -0.23372477468141994
		;
createNode parentConstraint -n "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidUpper_00_Part_CtrlPosition_GRP";
	rename -uid "36B9E85C-4C1B-D8F0-24F8-31B9623FA155";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -2.0917415618896484 8.615190713301752 8.0394248962402344 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidUpper_00_Part_CtrlPosition_GRP";
	rename -uid "5CEF9EC3-4F96-427C-F992-6281A2376F3C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidUpper_01_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "ACAD31CB-4BE5-13DD-0ACE-EBBFE0FA7198";
createNode transform -n "R_LidUpper_01_Part_CtrlPosition" -p "R_LidUpper_01_Part_CtrlPosition_GRP";
	rename -uid "C19A2FF7-4B13-21D0-C184-66847EC8FF4E";
createNode nurbsCurve -n "R_LidUpper_01_Part_CtrlPositionShape" -p "R_LidUpper_01_Part_CtrlPosition";
	rename -uid "73F0118B-43EB-3EA8-53E1-FAA61F16F59D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830873 0.27195253132676456 -0.23372477468141906
		0 0.31402373433661612 -0.23372477468141906
		-0.15701186716830873 0.27195253132676722 -0.23372477468141906
		-0.27195253132676589 0.15701186716830939 -0.23372477468141906
		-0.31402373433661679 0 -0.23372477468141906
		-0.27195253132676589 -0.016921620569736007 -0.23372477468141906
		-0.15701186716830873 -0.016922769976348562 -0.23372477468141906
		0 -0.01692319068836845 -0.23372477468141906
		0.15701186716830806 -0.016922769976348562 -0.23372477468141906
		0.27195253132676589 -0.016921620569736007 -0.23372477468141906
		0.31402373433661679 0 -0.23372477468141906
		0.27195253132676589 0.15701186716830939 -0.23372477468141906
		0.15701186716830873 0.27195253132676456 -0.23372477468141906
		0 0.31402373433661612 -0.23372477468141906
		-0.15701186716830873 0.27195253132676722 -0.23372477468141906
		;
createNode parentConstraint -n "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidUpper_01_Part_CtrlPosition_GRP";
	rename -uid "43A06773-4E8A-BB4D-EC52-2B87C3FE4DA4";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 4.4408920985006262e-016 0 0 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.3179900646209721 8.615190713301752 7.9887332916259766 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidUpper_01_Part_CtrlPosition_GRP";
	rename -uid "573D8288-493C-BA53-3EB2-12AE2F42BE19";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidUpper_02_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "01E0582E-4D72-635A-206A-53A8E572668D";
createNode transform -n "R_LidUpper_02_Part_CtrlPosition" -p "R_LidUpper_02_Part_CtrlPosition_GRP";
	rename -uid "863C9E6B-4367-E3E8-20D7-FDAFBC9CF046";
createNode nurbsCurve -n "R_LidUpper_02_Part_CtrlPositionShape" -p "R_LidUpper_02_Part_CtrlPosition";
	rename -uid "F7E08867-4C38-C495-D6AB-18B7B83CBEC3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830806 0.27195253132676456 -0.23372477468141994
		-1.3322676295501878e-015 0.31402373433661612 -0.23372477468141994
		-0.15701186716830939 0.27195253132676722 -0.23372477468141994
		-0.27195253132676722 0.15701186716830939 -0.23372477468141994
		-0.31402373433661879 0 -0.23372477468141994
		-0.27195253132676722 -0.016921620569736007 -0.23372477468141994
		-0.15701186716830939 -0.016922769976348562 -0.23372477468141994
		-1.3322676295501878e-015 -0.01692319068836845 -0.23372477468141994
		0.15701186716830673 -0.016922769976348562 -0.23372477468141994
		0.27195253132676456 -0.016921620569736007 -0.23372477468141994
		0.31402373433661612 0 -0.23372477468141994
		0.27195253132676456 0.15701186716830939 -0.23372477468141994
		0.15701186716830806 0.27195253132676456 -0.23372477468141994
		-1.3322676295501878e-015 0.31402373433661612 -0.23372477468141994
		-0.15701186716830939 0.27195253132676722 -0.23372477468141994
		;
createNode parentConstraint -n "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidUpper_02_Part_CtrlPosition_GRP";
	rename -uid "47EFBED8-4428-753A-2BA6-188CB243580B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 8.8817841970012523e-016 0 -8.8817841970012523e-016 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.4987268447875985 8.615190713301752 7.2066859685625957 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidUpper_02_Part_CtrlPosition_GRP";
	rename -uid "AB20ED4F-4A13-58B0-1B89-159AE67A5FCD";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidUpper_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidLower_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "DC5F8440-4B90-4B25-6879-D7A1E7E96B5C";
createNode transform -n "R_LidLower_00_Part_CtrlPosition" -p "R_LidLower_00_Part_CtrlPosition_GRP";
	rename -uid "88ABA157-406B-03BA-F715-9798FC44F170";
createNode nurbsCurve -n "R_LidLower_00_Part_CtrlPositionShape" -p "R_LidLower_00_Part_CtrlPosition";
	rename -uid "2337A318-474E-17A3-B8D0-FF8144638FC4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830873 -0.27195253132676456 -0.23372477468141994
		0 -0.31402373433661612 -0.23372477468141994
		-0.15701186716830839 -0.27195253132676722 -0.23372477468141994
		-0.27195253132676589 -0.15701186716830939 -0.23372477468141994
		-0.31402373433661679 0 -0.23372477468141994
		-0.27195253132676622 0.016921620569736007 -0.23372477468141994
		-0.15701186716830873 0.016922769976348562 -0.23372477468141994
		0 0.01692319068836845 -0.23372477468141994
		0.15701186716830806 0.016922769976348562 -0.23372477468141994
		0.27195253132676589 0.016921620569736007 -0.23372477468141994
		0.31402373433661679 0 -0.23372477468141994
		0.27195253132676589 -0.15701186716830939 -0.23372477468141994
		0.15701186716830873 -0.27195253132676456 -0.23372477468141994
		0 -0.31402373433661612 -0.23372477468141994
		-0.15701186716830839 -0.27195253132676722 -0.23372477468141994
		;
createNode parentConstraint -n "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidLower_00_Part_CtrlPosition_GRP";
	rename -uid "6DA25A58-4845-F6D7-04DE-39827561E39E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidLower_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -2.0934193134307861 8.2652094053183536 7.9774303436279297 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidLower_00_Part_CtrlPosition_GRP";
	rename -uid "C4614D44-410F-3B79-2D92-9CA7DAC08BD6";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidLower_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidLower_01_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "BD2718DB-4E3C-1224-704D-398AF56728D4";
createNode transform -n "R_LidLower_01_Part_CtrlPosition" -p "R_LidLower_01_Part_CtrlPosition_GRP";
	rename -uid "3D190807-495F-2184-E2C3-D7A815D9B58A";
createNode nurbsCurve -n "R_LidLower_01_Part_CtrlPositionShape" -p "R_LidLower_01_Part_CtrlPosition";
	rename -uid "C5692CBF-4719-8D4A-FEC2-D9B46C89092B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830873 -0.27195253132676456 -0.23372477468141861
		0 -0.31402373433661612 -0.23372477468141861
		-0.15701186716830873 -0.27195253132676722 -0.23372477468141861
		-0.27195253132676589 -0.15701186716830939 -0.23372477468141861
		-0.31402373433661679 0 -0.23372477468141861
		-0.27195253132676589 0.016921620569736007 -0.23372477468141861
		-0.15701186716830873 0.016922769976348562 -0.23372477468141861
		0 0.01692319068836845 -0.23372477468141861
		0.15701186716830806 0.016922769976348562 -0.23372477468141861
		0.27195253132676589 0.016921620569736007 -0.23372477468141861
		0.31402373433661679 0 -0.23372477468141861
		0.27195253132676589 -0.15701186716830939 -0.23372477468141861
		0.15701186716830873 -0.27195253132676456 -0.23372477468141861
		0 -0.31402373433661612 -0.23372477468141861
		-0.15701186716830873 -0.27195253132676722 -0.23372477468141861
		;
createNode parentConstraint -n "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidLower_01_Part_CtrlPosition_GRP";
	rename -uid "6C8E3925-4E9E-BCBE-DB2A-25A1B9DA4CD3";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -8.8817841970012523e-016 -1.7763568394002505e-015 
		-8.8817841970012523e-016 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.3083300590515128 8.2652094053183518 7.9009857177734384 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidLower_01_Part_CtrlPosition_GRP";
	rename -uid "CB1A6363-44D6-D902-0830-8ABBE521A899";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidLower_01_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidLower_02_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "A1EB429E-4489-C7CD-5D1B-12B2CB428A20";
createNode transform -n "R_LidLower_02_Part_CtrlPosition" -p "R_LidLower_02_Part_CtrlPosition_GRP";
	rename -uid "25E5D816-45C7-425E-22C2-68BEF34585CA";
createNode nurbsCurve -n "R_LidLower_02_Part_CtrlPositionShape" -p "R_LidLower_02_Part_CtrlPosition";
	rename -uid "68EA351A-4CEC-F033-8A2E-30B9DF47B89C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.15701186716830939 -0.27195253132676456 -0.23372477468141994
		0 -0.31402373433661612 -0.23372477468141994
		-0.15701186716830806 -0.27195253132676722 -0.23372477468141994
		-0.27195253132676589 -0.15701186716830939 -0.23372477468141994
		-0.31402373433661745 0 -0.23372477468141994
		-0.27195253132676589 0.016921620569736007 -0.23372477468141994
		-0.15701186716830806 0.016922769976348562 -0.23372477468141994
		0 0.01692319068836845 -0.23372477468141994
		0.15701186716830806 0.016922769976348562 -0.23372477468141994
		0.27195253132676589 0.016921620569736007 -0.23372477468141994
		0.31402373433661745 0 -0.23372477468141994
		0.27195253132676589 -0.15701186716830939 -0.23372477468141994
		0.15701186716830939 -0.27195253132676456 -0.23372477468141994
		0 -0.31402373433661612 -0.23372477468141994
		-0.15701186716830806 -0.27195253132676722 -0.23372477468141994
		;
createNode parentConstraint -n "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidLower_02_Part_CtrlPosition_GRP";
	rename -uid "DA2DD98C-4312-C839-7E54-BEBD17D58EA0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidLower_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -8.8817841970012523e-016 0 8.8817841970012523e-016 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.4987268447875968 8.2652094053183536 7.1507586919512658 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidLower_02_Part_CtrlPosition_GRP";
	rename -uid "62FFE044-45DA-4A95-EB22-DA87EA3DCD99";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidLower_02_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketUpper_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "8392C6C2-4FED-2AD6-3DF2-BB860C3D54F3";
createNode transform -n "R_SocketUpper_00_Part_CtrlPosition" -p "R_SocketUpper_00_Part_CtrlPosition_GRP";
	rename -uid "C5E17F4C-4DC3-2046-F896-E28A82934ABB";
createNode nurbsCurve -n "R_SocketUpper_00_Part_CtrlPositionShape" -p "R_SocketUpper_00_Part_CtrlPosition";
	rename -uid "9794107F-4134-E344-694D-D4A943F54276";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838931 0.11466059452736133 -0.31669768687164357
		-0.25335102051838931 -0.11466059452736133 -0.31669768687164357
		0.25335102051838909 -0.11466059452736133 -0.31669768687164357
		0.25335102051838909 0.11466059452736133 -0.31669768687164357
		-0.25335102051838931 0.11466059452736133 -0.31669768687164357
		;
createNode parentConstraint -n "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketUpper_00_Part_CtrlPosition_GRP";
	rename -uid "0221F11B-43CF-282D-0B4D-CCB8A14932CB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketUpper_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -1.7763568394002505e-015 0 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -2.0917415618896484 9.1716892260193692 8.280426025390625 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketUpper_00_Part_CtrlPosition_GRP";
	rename -uid "8A58DB24-484D-2588-BB30-79BBA6ADBD7C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketUpper_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketUpper_01_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "A4A004D7-4AC6-6717-0827-D79A827551FB";
createNode transform -n "R_SocketUpper_01_Part_CtrlPosition" -p "R_SocketUpper_01_Part_CtrlPosition_GRP";
	rename -uid "CDF90999-4468-03EB-9773-E098A86ED4EB";
createNode nurbsCurve -n "R_SocketUpper_01_Part_CtrlPositionShape" -p "R_SocketUpper_01_Part_CtrlPosition";
	rename -uid "D87114E9-470E-71F1-1D53-8C9B95E0F67E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838954 0.11466059452736133 -0.31669768687164357
		-0.25335102051838954 -0.11466059452736133 -0.31669768687164357
		0.25335102051838865 -0.11466059452736133 -0.31669768687164357
		0.25335102051838865 0.11466059452736133 -0.31669768687164357
		-0.25335102051838954 0.11466059452736133 -0.31669768687164357
		;
createNode parentConstraint -n "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketUpper_01_Part_CtrlPosition_GRP";
	rename -uid "8CFEAA39-40B6-ABD9-AA7C-0F9AF0D9547E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketUpper_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 4.4408920985006262e-016 -1.7763568394002505e-015 
		0 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.3179900646209721 9.1716892260193692 8.0734004974365234 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketUpper_01_Part_CtrlPosition_GRP";
	rename -uid "6C94F570-4F17-CE67-CCA2-7E8FB16B884C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketUpper_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketUpper_02_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "EBC63DAE-4014-89E8-3BFE-AFB9F08DABFB";
createNode transform -n "R_SocketUpper_02_Part_CtrlPosition" -p "R_SocketUpper_02_Part_CtrlPosition_GRP";
	rename -uid "45726F19-41D2-0135-6427-008A23B1F94C";
createNode nurbsCurve -n "R_SocketUpper_02_Part_CtrlPositionShape" -p "R_SocketUpper_02_Part_CtrlPosition";
	rename -uid "B53386D3-413E-C04E-AFF7-A2B8A2AA8098";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838909 0.11466059452736133 -0.31669768687164357
		-0.25335102051838909 -0.11466059452736133 -0.31669768687164357
		0.25335102051838909 -0.11466059452736133 -0.31669768687164357
		0.25335102051838909 0.11466059452736133 -0.31669768687164357
		-0.25335102051838909 0.11466059452736133 -0.31669768687164357
		;
createNode parentConstraint -n "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketUpper_02_Part_CtrlPosition_GRP";
	rename -uid "1F482C20-4315-0AD1-13CB-AD80C084034A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketUpper_02_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -1.7763568394002505e-015 -8.8817841970012523e-016 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.4987268447875977 9.1716892260193692 7.3598788098301391 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketUpper_02_Part_CtrlPosition_GRP";
	rename -uid "43F24FDE-4921-66E3-6EA1-449B209E0DCF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketUpper_02_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketLower_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "7FA6D158-4BCD-1B43-DC87-2EABCD36C3BB";
createNode transform -n "R_SocketLower_00_Part_CtrlPosition" -p "R_SocketLower_00_Part_CtrlPosition_GRP";
	rename -uid "22FDE53F-4212-2CA3-44C2-79B483A71F1E";
createNode nurbsCurve -n "R_SocketLower_00_Part_CtrlPositionShape" -p "R_SocketLower_00_Part_CtrlPosition";
	rename -uid "6223B6A9-426C-E739-2FE1-CB90278520F9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838909 0.11466059452736133 -0.31669768687164357
		-0.25335102051838909 -0.11466059452736133 -0.31669768687164357
		0.25335102051838909 -0.11466059452736133 -0.31669768687164357
		0.25335102051838909 0.11466059452736133 -0.31669768687164357
		-0.25335102051838909 0.11466059452736133 -0.31669768687164357
		;
createNode parentConstraint -n "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketLower_00_Part_CtrlPosition_GRP";
	rename -uid "EBF6F061-4ED7-7CEB-7364-889F171B8BD9";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketLower_02_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.4987268447875977 7.71017785963177 7.0099451855625601 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketLower_00_Part_CtrlPosition_GRP";
	rename -uid "11299F01-4816-E651-752C-DC94BF62445D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketLower_02_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketLower_01_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "66E9DFB8-442E-25CC-C272-4E97345027A9";
createNode transform -n "R_SocketLower_01_Part_CtrlPosition" -p "R_SocketLower_01_Part_CtrlPosition_GRP";
	rename -uid "CB6DEFEE-47A8-57ED-9DCE-2A9C25EC0F1A";
createNode nurbsCurve -n "R_SocketLower_01_Part_CtrlPositionShape" -p "R_SocketLower_01_Part_CtrlPosition";
	rename -uid "FA3F7CFC-4A0A-A30E-81AC-85975846E414";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838776 0.1146605945273631 -0.31669768687164535
		-0.25335102051838776 -0.11466059452735955 -0.31669768687164535
		0.25335102051839042 -0.11466059452735955 -0.31669768687164535
		0.25335102051839042 0.1146605945273631 -0.31669768687164535
		-0.25335102051838776 0.1146605945273631 -0.31669768687164535
		;
createNode parentConstraint -n "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketLower_01_Part_CtrlPosition_GRP";
	rename -uid "A0E95AF5-48FB-7B77-CFA8-FF80586C7251";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketLower_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 4.4408920985006262e-016 0 -8.8817841970012523e-016 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -3.3083300590515141 7.71017785963177 7.603588581085206 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketLower_01_Part_CtrlPosition_GRP";
	rename -uid "6F610EA5-41B6-DB89-AEA8-B283CD2739B0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketLower_01_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketLower_02_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "D5EDCD91-4770-1EE7-BA6E-11B2DB6ACC46";
createNode transform -n "R_SocketLower_02_Part_CtrlPosition" -p "R_SocketLower_02_Part_CtrlPosition_GRP";
	rename -uid "852C9FF6-4D45-B1E2-84C2-A3BF8BA9684B";
createNode nurbsCurve -n "R_SocketLower_02_Part_CtrlPositionShape" -p "R_SocketLower_02_Part_CtrlPosition";
	rename -uid "96CF9F45-4FD7-4999-924B-B2AB14E47AA5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.25335102051838909 0.11466059452736133 -0.31669768687164357
		-0.25335102051838909 -0.11466059452736133 -0.31669768687164357
		0.25335102051838909 -0.11466059452736133 -0.31669768687164357
		0.25335102051838909 0.11466059452736133 -0.31669768687164357
		-0.25335102051838909 0.11466059452736133 -0.31669768687164357
		;
createNode parentConstraint -n "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketLower_02_Part_CtrlPosition_GRP";
	rename -uid "9096D299-4250-DE36-49AB-6B92AB35493F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketLower_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -2.0934193134307861 7.71017785963177 7.840672492980957 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketLower_02_Part_CtrlPosition_GRP";
	rename -uid "21D19A96-4750-489B-08DC-CFBD1A0919BB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketLower_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidInner_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "27815B21-46D6-AF11-A023-8AB3B552BF09";
createNode transform -n "R_LidInner_00_Part_CtrlPosition" -p "R_LidInner_00_Part_CtrlPosition_GRP";
	rename -uid "8CF246B4-44B9-4EDE-0FB6-3AA43E1E5981";
createNode nurbsCurve -n "R_LidInner_00_Part_CtrlPositionShape" -p "R_LidInner_00_Part_CtrlPosition";
	rename -uid "957B199B-46AF-8E4B-9181-2DA30A89023D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		-0.29033203672200725 0.15701186716831206 -0.17155172947280306
		-0.33240323973185848 2.6645352591003757e-015 -0.17155172947280306
		-0.29033203672200725 -0.15701186716830673 -0.17155172947280306
		-0.17539137256355009 -0.27195253132676456 -0.17155172947280306
		-0.018379505395241358 -0.31402373433661612 -0.17155172947280306
		-0.0014578848255050181 -0.27195253132676456 -0.17155172947280306
		-0.0014567354188924631 -0.15701186716830673 -0.17155172947280306
		-0.0014563147068732407 2.6645352591003757e-015 -0.17155172947280306
		-0.0014567354188924631 0.15701186716830939 -0.17155172947280306
		-0.0014578848255050181 0.27195253132676722 -0.17155172947280306
		-0.018379505395241025 0.31402373433661879 -0.17155172947280306
		-0.17539137256354975 0.27195253132676722 -0.17155172947280306
		-0.29033203672200725 0.15701186716831206 -0.17155172947280306
		-0.33240323973185848 2.6645352591003757e-015 -0.17155172947280306
		-0.29033203672200725 -0.15701186716830673 -0.17155172947280306
		;
createNode parentConstraint -n "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidInner_00_Part_CtrlPosition_GRP";
	rename -uid "38AEDB2A-4715-8072-43E0-818A3CB0194B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidInner_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -1.7763568394002505e-015 0 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -1.6553013324737549 8.4373177475072563 7.8856148719787598 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidInner_00_Part_CtrlPosition_GRP";
	rename -uid "E7C04D6F-4160-2557-2397-03BF07A67D5F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidInner_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_LidOuter_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "FB9A30D1-4146-5EF7-441A-2E80A929C92D";
createNode transform -n "R_LidOuter_00_Part_CtrlPosition" -p "R_LidOuter_00_Part_CtrlPosition_GRP";
	rename -uid "F3398B16-4CEE-0CC5-6EE0-2C9B25E87B27";
createNode nurbsCurve -n "R_LidOuter_00_Part_CtrlPositionShape" -p "R_LidOuter_00_Part_CtrlPosition";
	rename -uid "5E94D396-4986-C272-0FA5-72935F283DEE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		0.29589458670430968 -0.15701186716831206 -0.17155172947280306
		0.33796578971416125 -2.6645352591003757e-015 -0.17155172947280306
		0.29589458670431101 0.15701186716830673 -0.17155172947280306
		0.18095392254585319 0.27195253132676456 -0.17155172947280306
		0.023942055377545124 0.31402373433661612 -0.17155172947280306
		0.0070204348078077849 0.27195253132676456 -0.17155172947280306
		0.0070192854011952299 0.15701186716830673 -0.17155172947280306
		0.0070188646891766737 -2.6645352591003757e-015 -0.17155172947280306
		0.0070192854011952299 -0.15701186716830939 -0.17155172947280306
		0.0070204348078077849 -0.27195253132676722 -0.17155172947280306
		0.023942055377543792 -0.31402373433661879 -0.17155172947280306
		0.18095392254585319 -0.27195253132676722 -0.17155172947280306
		0.29589458670430968 -0.15701186716831206 -0.17155172947280306
		0.33796578971416125 -2.6645352591003757e-015 -0.17155172947280306
		0.29589458670431101 0.15701186716830673 -0.17155172947280306
		;
createNode parentConstraint -n "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_LidOuter_00_Part_CtrlPosition_GRP";
	rename -uid "DCB0898F-4697-3B4F-251D-2FBF4ABFF0AD";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -4.876265968638287 8.437317747507258 6.7999181648650051 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_LidOuter_00_Part_CtrlPosition_GRP";
	rename -uid "2D7C23EA-4EC3-1682-FD26-8A83759D1C18";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_LidOuter_00_SkeletonW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketInner_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "8B488744-4415-27BE-EA35-73AE1DFB96E8";
createNode transform -n "R_SocketInner_00_Part_CtrlPosition" -p "R_SocketInner_00_Part_CtrlPosition_GRP";
	rename -uid "04376406-49DB-49C7-C956-4EB0A71DD8FC";
createNode nurbsCurve -n "R_SocketInner_00_Part_CtrlPositionShape" -p "R_SocketInner_00_Part_CtrlPosition";
	rename -uid "ACB4535C-42B6-2027-94FA-ECACE0C0F6E4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.11466059452736177 -0.25335102051839264 -0.31669768687164357
		0.1146605945273611 -0.25335102051839264 -0.31669768687164357
		0.11466059452736088 0.25335102051838554 -0.31669768687164357
		-0.11466059452736199 0.25335102051838554 -0.31669768687164357
		-0.11466059452736177 -0.25335102051839264 -0.31669768687164357
		;
createNode parentConstraint -n "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketInner_00_Part_CtrlPosition_GRP";
	rename -uid "45DE91F0-4A37-A6D9-22DF-699533E00FAB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketInner_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -2.2204460492503131e-016 -1.7763568394002505e-015 
		0 ;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -1.2401901235847821 8.4420241746844216 8.0583465244996688 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketInner_00_Part_CtrlPosition_GRP";
	rename -uid "E2E673CE-4154-A52B-BABA-C192A4633463";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketInner_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "R_SocketOuter_00_Part_CtrlPosition_GRP" -p "Facial_CtrlsSpace_GRP";
	rename -uid "E6D39758-430B-D091-91E9-D381DAEF3E8A";
createNode transform -n "R_SocketOuter_00_Part_CtrlPosition" -p "R_SocketOuter_00_Part_CtrlPosition_GRP";
	rename -uid "10EA1303-4EB3-BA94-C19C-43B0397A113E";
createNode nurbsCurve -n "R_SocketOuter_00_Part_CtrlPositionShape" -p "R_SocketOuter_00_Part_CtrlPosition";
	rename -uid "FFDF3476-4A63-D7DE-5372-0498F977BFD2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.11466059452736133 -0.25335102051838909 -0.31669768687164357
		0.11466059452736133 -0.25335102051838909 -0.31669768687164357
		0.11466059452736133 0.25335102051838909 -0.31669768687164357
		-0.11466059452736133 0.25335102051838909 -0.31669768687164357
		-0.11466059452736133 -0.25335102051838909 -0.31669768687164357
		;
createNode parentConstraint -n "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1" 
		-p "R_SocketOuter_00_Part_CtrlPosition_GRP";
	rename -uid "6D8C9EEC-4964-CB5F-74E4-93B963358658";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketOuter_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 0 180 0 ;
	setAttr ".rst" -type "double3" -5.2656780232713203 8.437317747507258 6.3903667231273822 ;
	setAttr ".rsrr" -type "double3" 0 180 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1" 
		-p "R_SocketOuter_00_Part_CtrlPosition_GRP";
	rename -uid "B7151C2E-4649-BAA0-E71D-259A0FE7AF67";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "R_SocketOuter_00_SkeletonW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "Facial_Lattice_CTL_GRP" -p "M_Head_Position";
	rename -uid "1F67B8BE-4C0A-E173-8D44-C5A572EE2885";
	setAttr -l on ".v" no;
	setAttr ".t" -type "double3" 0 6.1473499966045049 4.3422248624220812 ;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "Facial_Lattice_CTL" -p "Facial_Lattice_CTL_GRP";
	rename -uid "EDA902D5-4847-9474-D22A-B3B073E020A0";
	setAttr ".ovc" 17;
createNode nurbsCurve -n "Facial_Lattice_CTLShape" -p "Facial_Lattice_CTL";
	rename -uid "723AC9F5-4203-D512-80B4-34A8A5569AB3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 59 0 no 3
		60 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59
		60
		-4.2225703937779711e-017 -5.9259849213566704e-016 3.8526095173852126e-015
		-4.2225703937779711e-017 -5.9259849213566704e-016 -4.5640239484713945
		-7.3522591503601524e-017 -0.38033532903928374 -4.183688619432111
		-4.2225703937779711e-017 -5.9259849213566704e-016 -4.5640239484713945
		7.4267372278627475e-017 0.38033532903928252 -4.183688619432111
		-4.2225703937779711e-017 -5.9259849213566704e-016 -4.5640239484713945
		-0.38033532903928319 -5.9403729810670955e-016 -4.183688619432111
		-4.2225703937779711e-017 -5.9259849213566704e-016 -4.5640239484713945
		0.38033532903928313 -6.4681942802893423e-016 -4.183688619432111
		-4.2225703937779711e-017 -5.9259849213566704e-016 -4.5640239484713945
		-4.2225703937779711e-017 -5.9259849213566704e-016 3.8526095173852126e-015
		1.7983163212307672e-016 -4.5640239484713989 3.8526095173852126e-015
		-3.2687681513027982e-016 -4.1836886194321155 -0.38033532903927936
		1.7983163212307672e-016 -4.5640239484713989 3.8526095173852126e-015
		-3.2687681513027982e-016 -4.1836886194321155 0.38033532903928702
		1.7983163212307672e-016 -4.5640239484713989 3.8526095173852126e-015
		-0.38033532903928197 -4.1836886194321137 3.8526095173852126e-015
		1.7983163212307672e-016 -4.5640239484713989 3.8526095173852126e-015
		0.38033532903928241 -4.1836886194321155 3.8526095173852126e-015
		1.7983163212307672e-016 -4.5640239484713989 3.8526095173852126e-015
		-4.2225703937779711e-017 -5.9259849213566704e-016 3.8526095173852126e-015
		-4.2225703937779711e-017 -5.9259849213566704e-016 4.5640239484714025
		-7.3522591503601524e-017 -0.38033532903928374 4.183688619432119
		-4.2225703937779711e-017 -5.9259849213566704e-016 4.5640239484714025
		7.4267372278627475e-017 0.38033532903928252 4.183688619432119
		-4.2225703937779711e-017 -5.9259849213566704e-016 4.5640239484714025
		-0.38033532903928319 -5.9403729810670955e-016 4.183688619432119
		-4.2225703937779711e-017 -5.9259849213566704e-016 4.5640239484714025
		0.38033532903928324 -3.9826500391135319e-015 4.1836886194321234
		-4.2225703937780414e-017 -3.9706548071580464e-015 4.564023948471406
		-4.2225703937780414e-017 -3.9706548071580464e-015 3.8526095173852126e-015
		-1.5797399937916097e-016 4.5640239484713989 3.8526095173852126e-015
		3.4873444787419566e-016 4.1836886194321155 -0.38033532903927936
		-1.5797399937916097e-016 4.5640239484713989 3.8526095173852126e-015
		3.4873444787419566e-016 4.1836886194321155 0.38033532903928702
		3.4873444787419566e-016 4.1836886194321155 0.38033532903928702
		-1.5797399937916097e-016 4.5640239484713989 3.8526095173852126e-015
		-0.38033532903928241 4.1836886194321155 3.8526095173852126e-015
		-1.5797399937916097e-016 4.5640239484713989 3.8526095173852126e-015
		0.38033532903928197 4.1836886194321137 3.8526095173852126e-015
		-1.5797399937916097e-016 4.5640239484713989 3.8526095173852126e-015
		-4.2225703937779711e-017 -5.9259849213566704e-016 3.8526095173852126e-015
		-4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		-4.1836886194321155 -5.5037278819788729e-016 -0.38033532903927936
		-4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		-4.1836886194321155 -5.5037278819788729e-016 0.38033532903928702
		-4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		-4.1836886194321155 0.38033532903928263 3.8526095173852126e-015
		-4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		-4.1836886194321155 -0.3803353290392838 3.8526095173852126e-015
		-4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		0 -5.5037278819788729e-016 3.8526095173852126e-015
		4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		4.1836886194321155 -5.5037278819788729e-016 -0.38033532903927936
		4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		4.1836886194321155 -5.5037278819788729e-016 0.38033532903928702
		4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		4.1836886194321155 0.38033532903928263 3.8526095173852126e-015
		4.5640239484713989 -5.5037278819788729e-016 3.8526095173852126e-015
		4.1836886194321155 -0.3803353290392838 3.8526095173852126e-015
		;
createNode transform -n "Facial_Lattice_GRP" -p "Facial_Lattice_CTL";
	rename -uid "5874063B-4967-96A6-1AC7-DFA09987619B";
	setAttr ".t" -type "double3" 0 0 8.8817841970012523e-016 ;
	setAttr ".s" -type "double3" 13 13 13 ;
createNode transform -n "Facial_Lattice" -p "Facial_Lattice_GRP";
	rename -uid "BC76F06B-4061-9670-387C-F6A674A58BBC";
	setAttr ".v" no;
createNode lattice -n "Facial_LatticeShape" -p "Facial_Lattice";
	rename -uid "3CEDE053-40D3-B52A-194B-17A8224B2262";
	setAttr -k off ".v";
	setAttr ".tw" yes;
	setAttr ".sd" 7;
	setAttr ".td" 7;
	setAttr ".ud" 7;
createNode lattice -n "Facial_LatticeShapeOrig" -p "Facial_Lattice";
	rename -uid "0A0B0810-498D-B438-CF9E-C0BC99A75EA1";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".sd" 7;
	setAttr ".td" 7;
	setAttr ".ud" 7;
	setAttr ".cc" -type "lattice" 7 7 7 343 -0.5 -0.5 -0.5 -0.33333333333333337
		 -0.5 -0.5 -0.16666666666666671 -0.5 -0.5 -5.5511151231257827e-017 -0.5 -0.5 0.1666666666666666
		 -0.5 -0.5 0.33333333333333326 -0.5 -0.5 0.49999999999999989 -0.5 -0.5 -0.5 -0.33333333333333337
		 -0.5 -0.33333333333333337 -0.33333333333333337 -0.5 -0.16666666666666671 -0.33333333333333337
		 -0.5 -5.5511151231257827e-017 -0.33333333333333337 -0.5 0.1666666666666666 -0.33333333333333337
		 -0.5 0.33333333333333326 -0.33333333333333337 -0.5 0.49999999999999989 -0.33333333333333337
		 -0.5 -0.5 -0.16666666666666671 -0.5 -0.33333333333333337 -0.16666666666666671 -0.5 -0.16666666666666671
		 -0.16666666666666671 -0.5 -5.5511151231257827e-017 -0.16666666666666671 -0.5 0.1666666666666666
		 -0.16666666666666671 -0.5 0.33333333333333326 -0.16666666666666671 -0.5 0.49999999999999989
		 -0.16666666666666671 -0.5 -0.5 -5.5511151231257827e-017 -0.5 -0.33333333333333337
		 -5.5511151231257827e-017 -0.5 -0.16666666666666671 -5.5511151231257827e-017 -0.5 -5.5511151231257827e-017
		 -5.5511151231257827e-017 -0.5 0.1666666666666666 -5.5511151231257827e-017 -0.5 0.33333333333333326
		 -5.5511151231257827e-017 -0.5 0.49999999999999989 -5.5511151231257827e-017 -0.5 -0.5
		 0.1666666666666666 -0.5 -0.33333333333333337 0.1666666666666666 -0.5 -0.16666666666666671
		 0.1666666666666666 -0.5 -5.5511151231257827e-017 0.1666666666666666 -0.5 0.1666666666666666
		 0.1666666666666666 -0.5 0.33333333333333326 0.1666666666666666 -0.5 0.49999999999999989
		 0.1666666666666666 -0.5 -0.5 0.33333333333333326 -0.5 -0.33333333333333337 0.33333333333333326
		 -0.5 -0.16666666666666671 0.33333333333333326 -0.5 -5.5511151231257827e-017 0.33333333333333326
		 -0.5 0.1666666666666666 0.33333333333333326 -0.5 0.33333333333333326 0.33333333333333326
		 -0.5 0.49999999999999989 0.33333333333333326 -0.5 -0.5 0.49999999999999989 -0.5 -0.33333333333333337
		 0.49999999999999989 -0.5 -0.16666666666666671 0.49999999999999989 -0.5 -5.5511151231257827e-017
		 0.49999999999999989 -0.5 0.1666666666666666 0.49999999999999989 -0.5 0.33333333333333326
		 0.49999999999999989 -0.5 0.49999999999999989 0.49999999999999989 -0.5 -0.5 -0.5 -0.33333333333333337 -0.33333333333333337
		 -0.5 -0.33333333333333337 -0.16666666666666671 -0.5 -0.33333333333333337 -5.5511151231257827e-017
		 -0.5 -0.33333333333333337 0.1666666666666666 -0.5 -0.33333333333333337 0.33333333333333326
		 -0.5 -0.33333333333333337 0.49999999999999989 -0.5 -0.33333333333333337 -0.5 -0.33333333333333337
		 -0.33333333333333337 -0.33333333333333337 -0.33333333333333337 -0.33333333333333337 -0.16666666666666671
		 -0.33333333333333337 -0.33333333333333337 -5.5511151231257827e-017 -0.33333333333333337
		 -0.33333333333333337 0.1666666666666666 -0.33333333333333337 -0.33333333333333337 0.33333333333333326
		 -0.33333333333333337 -0.33333333333333337 0.49999999999999989 -0.33333333333333337
		 -0.33333333333333337 -0.5 -0.16666666666666671 -0.33333333333333337 -0.33333333333333337
		 -0.16666666666666671 -0.33333333333333337 -0.16666666666666671 -0.16666666666666671
		 -0.33333333333333337 -5.5511151231257827e-017 -0.16666666666666671 -0.33333333333333337 0.1666666666666666
		 -0.16666666666666671 -0.33333333333333337 0.33333333333333326 -0.16666666666666671
		 -0.33333333333333337 0.49999999999999989 -0.16666666666666671 -0.33333333333333337 -0.5
		 -5.5511151231257827e-017 -0.33333333333333337 -0.33333333333333337 -5.5511151231257827e-017
		 -0.33333333333333337 -0.16666666666666671 -5.5511151231257827e-017 -0.33333333333333337 -5.5511151231257827e-017
		 -5.5511151231257827e-017 -0.33333333333333337 0.1666666666666666 -5.5511151231257827e-017
		 -0.33333333333333337 0.33333333333333326 -5.5511151231257827e-017 -0.33333333333333337 0.49999999999999989
		 -5.5511151231257827e-017 -0.33333333333333337 -0.5 0.1666666666666666 -0.33333333333333337 -0.33333333333333337
		 0.1666666666666666 -0.33333333333333337 -0.16666666666666671 0.1666666666666666 -0.33333333333333337 -5.5511151231257827e-017
		 0.1666666666666666 -0.33333333333333337 0.1666666666666666 0.1666666666666666 -0.33333333333333337 0.33333333333333326
		 0.1666666666666666 -0.33333333333333337 0.49999999999999989 0.1666666666666666 -0.33333333333333337 -0.5
		 0.33333333333333326 -0.33333333333333337 -0.33333333333333337 0.33333333333333326
		 -0.33333333333333337 -0.16666666666666671 0.33333333333333326 -0.33333333333333337 -5.5511151231257827e-017
		 0.33333333333333326 -0.33333333333333337 0.1666666666666666 0.33333333333333326 -0.33333333333333337 0.33333333333333326
		 0.33333333333333326 -0.33333333333333337 0.49999999999999989 0.33333333333333326
		 -0.33333333333333337 -0.5 0.49999999999999989 -0.33333333333333337 -0.33333333333333337
		 0.49999999999999989 -0.33333333333333337 -0.16666666666666671 0.49999999999999989
		 -0.33333333333333337 -5.5511151231257827e-017 0.49999999999999989 -0.33333333333333337 0.1666666666666666
		 0.49999999999999989 -0.33333333333333337 0.33333333333333326 0.49999999999999989
		 -0.33333333333333337 0.49999999999999989 0.49999999999999989 -0.33333333333333337 -0.5
		 -0.5 -0.16666666666666671 -0.33333333333333337 -0.5 -0.16666666666666671 -0.16666666666666671
		 -0.5 -0.16666666666666671 -5.5511151231257827e-017 -0.5 -0.16666666666666671 0.1666666666666666
		 -0.5 -0.16666666666666671 0.33333333333333326 -0.5 -0.16666666666666671 0.49999999999999989
		 -0.5 -0.16666666666666671 -0.5 -0.33333333333333337 -0.16666666666666671 -0.33333333333333337
		 -0.33333333333333337 -0.16666666666666671 -0.16666666666666671 -0.33333333333333337
		 -0.16666666666666671 -5.5511151231257827e-017 -0.33333333333333337 -0.16666666666666671 0.1666666666666666
		 -0.33333333333333337 -0.16666666666666671 0.33333333333333326 -0.33333333333333337
		 -0.16666666666666671 0.49999999999999989 -0.33333333333333337 -0.16666666666666671 -0.5
		 -0.16666666666666671 -0.16666666666666671 -0.33333333333333337 -0.16666666666666671
		 -0.16666666666666671 -0.16666666666666671 -0.16666666666666671 -0.16666666666666671 -5.5511151231257827e-017
		 -0.16666666666666671 -0.16666666666666671 0.1666666666666666 -0.16666666666666671
		 -0.16666666666666671 0.33333333333333326 -0.16666666666666671 -0.16666666666666671 0.49999999999999989
		 -0.16666666666666671 -0.16666666666666671 -0.5 -5.5511151231257827e-017 -0.16666666666666671 -0.33333333333333337
		 -5.5511151231257827e-017 -0.16666666666666671 -0.16666666666666671 -5.5511151231257827e-017
		 -0.16666666666666671 -5.5511151231257827e-017 -5.5511151231257827e-017 -0.16666666666666671 0.1666666666666666
		 -5.5511151231257827e-017 -0.16666666666666671 0.33333333333333326 -5.5511151231257827e-017
		 -0.16666666666666671 0.49999999999999989 -5.5511151231257827e-017 -0.16666666666666671 -0.5
		 0.1666666666666666 -0.16666666666666671 -0.33333333333333337 0.1666666666666666 -0.16666666666666671 -0.16666666666666671
		 0.1666666666666666 -0.16666666666666671 -5.5511151231257827e-017 0.1666666666666666
		 -0.16666666666666671 0.1666666666666666 0.1666666666666666 -0.16666666666666671 0.33333333333333326
		 0.1666666666666666 -0.16666666666666671 0.49999999999999989 0.1666666666666666 -0.16666666666666671 -0.5
		 0.33333333333333326 -0.16666666666666671 -0.33333333333333337 0.33333333333333326
		 -0.16666666666666671 -0.16666666666666671 0.33333333333333326 -0.16666666666666671 -5.5511151231257827e-017
		 0.33333333333333326 -0.16666666666666671 0.1666666666666666 0.33333333333333326 -0.16666666666666671 0.33333333333333326
		 0.33333333333333326 -0.16666666666666671 0.49999999999999989 0.33333333333333326
		 -0.16666666666666671 -0.5 0.49999999999999989 -0.16666666666666671 -0.33333333333333337
		 0.49999999999999989 -0.16666666666666671 -0.16666666666666671 0.49999999999999989
		 -0.16666666666666671 -5.5511151231257827e-017 0.49999999999999989 -0.16666666666666671 0.1666666666666666
		 0.49999999999999989 -0.16666666666666671 0.33333333333333326 0.49999999999999989
		 -0.16666666666666671 0.49999999999999989 0.49999999999999989 -0.16666666666666671 -0.5
		 -0.5 -5.5511151231257827e-017 -0.33333333333333337 -0.5 -5.5511151231257827e-017 -0.16666666666666671
		 -0.5 -5.5511151231257827e-017 -5.5511151231257827e-017 -0.5 -5.5511151231257827e-017 0.1666666666666666
		 -0.5 -5.5511151231257827e-017 0.33333333333333326 -0.5 -5.5511151231257827e-017 0.49999999999999989
		 -0.5 -5.5511151231257827e-017 -0.5 -0.33333333333333337 -5.5511151231257827e-017 -0.33333333333333337
		 -0.33333333333333337 -5.5511151231257827e-017 -0.16666666666666671 -0.33333333333333337
		 -5.5511151231257827e-017 -5.5511151231257827e-017 -0.33333333333333337 -5.5511151231257827e-017 0.1666666666666666
		 -0.33333333333333337 -5.5511151231257827e-017 0.33333333333333326 -0.33333333333333337
		 -5.5511151231257827e-017 0.49999999999999989 -0.33333333333333337 -5.5511151231257827e-017 -0.5
		 -0.16666666666666671 -5.5511151231257827e-017 -0.33333333333333337 -0.16666666666666671
		 -5.5511151231257827e-017 -0.16666666666666671 -0.16666666666666671 -5.5511151231257827e-017 -5.5511151231257827e-017
		 -0.16666666666666671 -5.5511151231257827e-017 0.1666666666666666 -0.16666666666666671
		 -5.5511151231257827e-017 0.33333333333333326 -0.16666666666666671 -5.5511151231257827e-017 0.49999999999999989
		 -0.16666666666666671 -5.5511151231257827e-017 -0.5 -5.5511151231257827e-017 -5.5511151231257827e-017 -0.33333333333333337
		 -5.5511151231257827e-017 -5.5511151231257827e-017 -0.16666666666666671 -5.5511151231257827e-017
		 -5.5511151231257827e-017 -5.5511151231257827e-017 -5.5511151231257827e-017 -5.5511151231257827e-017 0.1666666666666666
		 -5.5511151231257827e-017 -5.5511151231257827e-017 0.33333333333333326 -5.5511151231257827e-017
		 -5.5511151231257827e-017 0.49999999999999989 -5.5511151231257827e-017 -5.5511151231257827e-017 -0.5
		 0.1666666666666666 -5.5511151231257827e-017 -0.33333333333333337 0.1666666666666666
		 -5.5511151231257827e-017 -0.16666666666666671 0.1666666666666666 -5.5511151231257827e-017 -5.5511151231257827e-017
		 0.1666666666666666 -5.5511151231257827e-017 0.1666666666666666 0.1666666666666666
		 -5.5511151231257827e-017 0.33333333333333326 0.1666666666666666 -5.5511151231257827e-017 0.49999999999999989
		 0.1666666666666666 -5.5511151231257827e-017 -0.5 0.33333333333333326 -5.5511151231257827e-017 -0.33333333333333337
		 0.33333333333333326 -5.5511151231257827e-017 -0.16666666666666671 0.33333333333333326
		 -5.5511151231257827e-017 -5.5511151231257827e-017 0.33333333333333326 -5.5511151231257827e-017 0.1666666666666666
		 0.33333333333333326 -5.5511151231257827e-017 0.33333333333333326 0.33333333333333326
		 -5.5511151231257827e-017 0.49999999999999989 0.33333333333333326 -5.5511151231257827e-017 -0.5
		 0.49999999999999989 -5.5511151231257827e-017 -0.33333333333333337 0.49999999999999989
		 -5.5511151231257827e-017 -0.16666666666666671 0.49999999999999989 -5.5511151231257827e-017 -5.5511151231257827e-017
		 0.49999999999999989 -5.5511151231257827e-017 0.1666666666666666 0.49999999999999989
		 -5.5511151231257827e-017 0.33333333333333326 0.49999999999999989 -5.5511151231257827e-017 0.49999999999999989
		 0.49999999999999989 -5.5511151231257827e-017 -0.5 -0.5 0.1666666666666666 -0.33333333333333337
		 -0.5 0.1666666666666666 -0.16666666666666671 -0.5 0.1666666666666666 -5.5511151231257827e-017
		 -0.5 0.1666666666666666 0.1666666666666666 -0.5 0.1666666666666666 0.33333333333333326
		 -0.5 0.1666666666666666 0.49999999999999989 -0.5 0.1666666666666666 -0.5 -0.33333333333333337
		 0.1666666666666666 -0.33333333333333337 -0.33333333333333337 0.1666666666666666 -0.16666666666666671
		 -0.33333333333333337 0.1666666666666666 -5.5511151231257827e-017 -0.33333333333333337
		 0.1666666666666666 0.1666666666666666 -0.33333333333333337 0.1666666666666666 0.33333333333333326
		 -0.33333333333333337 0.1666666666666666 0.49999999999999989 -0.33333333333333337
		 0.1666666666666666 -0.5 -0.16666666666666671 0.1666666666666666 -0.33333333333333337
		 -0.16666666666666671 0.1666666666666666 -0.16666666666666671 -0.16666666666666671
		 0.1666666666666666 -5.5511151231257827e-017 -0.16666666666666671 0.1666666666666666 0.1666666666666666
		 -0.16666666666666671 0.1666666666666666 0.33333333333333326 -0.16666666666666671
		 0.1666666666666666 0.49999999999999989 -0.16666666666666671 0.1666666666666666 -0.5
		 -5.5511151231257827e-017 0.1666666666666666 -0.33333333333333337 -5.5511151231257827e-017
		 0.1666666666666666 -0.16666666666666671 -5.5511151231257827e-017 0.1666666666666666 -5.5511151231257827e-017
		 -5.5511151231257827e-017 0.1666666666666666 0.1666666666666666 -5.5511151231257827e-017
		 0.1666666666666666 0.33333333333333326 -5.5511151231257827e-017 0.1666666666666666 0.49999999999999989
		 -5.5511151231257827e-017 0.1666666666666666 -0.5 0.1666666666666666 0.1666666666666666 -0.33333333333333337
		 0.1666666666666666 0.1666666666666666 -0.16666666666666671 0.1666666666666666 0.1666666666666666 -5.5511151231257827e-017
		 0.1666666666666666 0.1666666666666666 0.1666666666666666 0.1666666666666666 0.1666666666666666 0.33333333333333326
		 0.1666666666666666 0.1666666666666666 0.49999999999999989 0.1666666666666666 0.1666666666666666 -0.5
		 0.33333333333333326 0.1666666666666666 -0.33333333333333337 0.33333333333333326 0.1666666666666666 -0.16666666666666671
		 0.33333333333333326 0.1666666666666666 -5.5511151231257827e-017 0.33333333333333326
		 0.1666666666666666 0.1666666666666666 0.33333333333333326 0.1666666666666666 0.33333333333333326
		 0.33333333333333326 0.1666666666666666 0.49999999999999989 0.33333333333333326 0.1666666666666666 -0.5
		 0.49999999999999989 0.1666666666666666 -0.33333333333333337 0.49999999999999989 0.1666666666666666 -0.16666666666666671
		 0.49999999999999989 0.1666666666666666 -5.5511151231257827e-017 0.49999999999999989
		 0.1666666666666666 0.1666666666666666 0.49999999999999989 0.1666666666666666 0.33333333333333326
		 0.49999999999999989 0.1666666666666666 0.49999999999999989 0.49999999999999989 0.1666666666666666 -0.5
		 -0.5 0.33333333333333326 -0.33333333333333337 -0.5 0.33333333333333326 -0.16666666666666671
		 -0.5 0.33333333333333326 -5.5511151231257827e-017 -0.5 0.33333333333333326 0.1666666666666666
		 -0.5 0.33333333333333326 0.33333333333333326 -0.5 0.33333333333333326 0.49999999999999989
		 -0.5 0.33333333333333326 -0.5 -0.33333333333333337 0.33333333333333326 -0.33333333333333337
		 -0.33333333333333337 0.33333333333333326 -0.16666666666666671 -0.33333333333333337
		 0.33333333333333326 -5.5511151231257827e-017 -0.33333333333333337 0.33333333333333326 0.1666666666666666
		 -0.33333333333333337 0.33333333333333326 0.33333333333333326 -0.33333333333333337
		 0.33333333333333326 0.49999999999999989 -0.33333333333333337 0.33333333333333326 -0.5
		 -0.16666666666666671 0.33333333333333326 -0.33333333333333337 -0.16666666666666671
		 0.33333333333333326 -0.16666666666666671 -0.16666666666666671 0.33333333333333326 -5.5511151231257827e-017
		 -0.16666666666666671 0.33333333333333326 0.1666666666666666 -0.16666666666666671
		 0.33333333333333326 0.33333333333333326 -0.16666666666666671 0.33333333333333326 0.49999999999999989
		 -0.16666666666666671 0.33333333333333326 -0.5 -5.5511151231257827e-017 0.33333333333333326 -0.33333333333333337
		 -5.5511151231257827e-017 0.33333333333333326 -0.16666666666666671 -5.5511151231257827e-017
		 0.33333333333333326 -5.5511151231257827e-017 -5.5511151231257827e-017 0.33333333333333326 0.1666666666666666
		 -5.5511151231257827e-017 0.33333333333333326 0.33333333333333326 -5.5511151231257827e-017
		 0.33333333333333326 0.49999999999999989 -5.5511151231257827e-017 0.33333333333333326 -0.5
		 0.1666666666666666 0.33333333333333326 -0.33333333333333337 0.1666666666666666 0.33333333333333326 -0.16666666666666671
		 0.1666666666666666 0.33333333333333326 -5.5511151231257827e-017 0.1666666666666666
		 0.33333333333333326 0.1666666666666666 0.1666666666666666 0.33333333333333326 0.33333333333333326
		 0.1666666666666666 0.33333333333333326 0.49999999999999989 0.1666666666666666 0.33333333333333326 -0.5
		 0.33333333333333326 0.33333333333333326 -0.33333333333333337 0.33333333333333326
		 0.33333333333333326 -0.16666666666666671 0.33333333333333326 0.33333333333333326 -5.5511151231257827e-017
		 0.33333333333333326 0.33333333333333326 0.1666666666666666 0.33333333333333326 0.33333333333333326 0.33333333333333326
		 0.33333333333333326 0.33333333333333326 0.49999999999999989 0.33333333333333326 0.33333333333333326 -0.5
		 0.49999999999999989 0.33333333333333326 -0.33333333333333337 0.49999999999999989
		 0.33333333333333326 -0.16666666666666671 0.49999999999999989 0.33333333333333326 -5.5511151231257827e-017
		 0.49999999999999989 0.33333333333333326 0.1666666666666666 0.49999999999999989 0.33333333333333326 0.33333333333333326
		 0.49999999999999989 0.33333333333333326 0.49999999999999989 0.49999999999999989 0.33333333333333326 -0.5
		 -0.5 0.49999999999999989 -0.33333333333333337 -0.5 0.49999999999999989 -0.16666666666666671
		 -0.5 0.49999999999999989 -5.5511151231257827e-017 -0.5 0.49999999999999989 0.1666666666666666
		 -0.5 0.49999999999999989 0.33333333333333326 -0.5 0.49999999999999989 0.49999999999999989
		 -0.5 0.49999999999999989 -0.5 -0.33333333333333337 0.49999999999999989 -0.33333333333333337
		 -0.33333333333333337 0.49999999999999989 -0.16666666666666671 -0.33333333333333337
		 0.49999999999999989 -5.5511151231257827e-017 -0.33333333333333337 0.49999999999999989 0.1666666666666666
		 -0.33333333333333337 0.49999999999999989 0.33333333333333326 -0.33333333333333337
		 0.49999999999999989 0.49999999999999989 -0.33333333333333337 0.49999999999999989 -0.5
		 -0.16666666666666671 0.49999999999999989 -0.33333333333333337 -0.16666666666666671
		 0.49999999999999989 -0.16666666666666671 -0.16666666666666671 0.49999999999999989 -5.5511151231257827e-017
		 -0.16666666666666671 0.49999999999999989 0.1666666666666666 -0.16666666666666671
		 0.49999999999999989 0.33333333333333326 -0.16666666666666671 0.49999999999999989 0.49999999999999989
		 -0.16666666666666671 0.49999999999999989 -0.5 -5.5511151231257827e-017 0.49999999999999989 -0.33333333333333337
		 -5.5511151231257827e-017 0.49999999999999989 -0.16666666666666671 -5.5511151231257827e-017
		 0.49999999999999989 -5.5511151231257827e-017 -5.5511151231257827e-017 0.49999999999999989 0.1666666666666666
		 -5.5511151231257827e-017 0.49999999999999989 0.33333333333333326 -5.5511151231257827e-017
		 0.49999999999999989 0.49999999999999989 -5.5511151231257827e-017 0.49999999999999989 -0.5
		 0.1666666666666666 0.49999999999999989 -0.33333333333333337 0.1666666666666666 0.49999999999999989 -0.16666666666666671
		 0.1666666666666666 0.49999999999999989 -5.5511151231257827e-017 0.1666666666666666
		 0.49999999999999989 0.1666666666666666 0.1666666666666666 0.49999999999999989 0.33333333333333326
		 0.1666666666666666 0.49999999999999989 0.49999999999999989 0.1666666666666666 0.49999999999999989 -0.5
		 0.33333333333333326 0.49999999999999989 -0.33333333333333337 0.33333333333333326
		 0.49999999999999989 -0.16666666666666671 0.33333333333333326 0.49999999999999989 -5.5511151231257827e-017
		 0.33333333333333326 0.49999999999999989 0.1666666666666666 0.33333333333333326 0.49999999999999989 0.33333333333333326
		 0.33333333333333326 0.49999999999999989 0.49999999999999989 0.33333333333333326 0.49999999999999989 -0.5
		 0.49999999999999989 0.49999999999999989 -0.33333333333333337 0.49999999999999989
		 0.49999999999999989 -0.16666666666666671 0.49999999999999989 0.49999999999999989 -5.5511151231257827e-017
		 0.49999999999999989 0.49999999999999989 0.1666666666666666 0.49999999999999989 0.49999999999999989 0.33333333333333326
		 0.49999999999999989 0.49999999999999989 0.49999999999999989 0.49999999999999989 0.49999999999999989 ;
createNode transform -n "Facial_LatticeBase" -p "Facial_Lattice_GRP";
	rename -uid "19A713A4-40C7-6DAA-D447-41BA4F557823";
createNode baseLattice -n "Facial_LatticeBaseShape" -p "Facial_LatticeBase";
	rename -uid "F9E5D632-4A8E-86F8-4AED-9182D128A9D7";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
createNode transform -n "Facial_LatticeLoc_GRP" -p "Facial_Lattice_CTL";
	rename -uid "0A890CF7-4757-C17A-4C55-3A86A158ACDA";
	setAttr ".t" -type "double3" 0 -6.1473499966045049 -4.3422248624220812 ;
createNode joint -n "LatticeJaw_00_LatticeLOC" -p "Facial_LatticeLoc_GRP";
	rename -uid "67B1143E-47FA-6F4D-522C-748174F5FB8D";
	setAttr ".t" -type "double3" 0 6.1021764032429999 4.3168233574683352 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".jo" -type "double3" 53.317649244106427 -7.7187903767794163e-015 -3.8751993851217785e-015 ;
	setAttr ".radi" 0.59514881453013457;
createNode joint -n "LatticeJaw_01_LatticeLOC" -p "LatticeJaw_00_LatticeLOC";
	rename -uid "79C6DFB9-46CF-5B58-FE76-35B937756EFB";
	setAttr ".t" -type "double3" -3.825385244698565e-016 0.21034094242777079 4.4387320462059474 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".jo" -type "double3" -8.3176492441063932 0 0 ;
	setAttr ".radi" 0.60975145792002983;
createNode joint -n "LatticeJaw_02_LatticeLOC" -p "LatticeJaw_01_LatticeLOC";
	rename -uid "442B4D13-44C0-F2EC-C696-DA97EB52BAFE";
	setAttr ".t" -type "double3" -7.5950159085697108e-016 0.051437749875716539 4.4531164339890594 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jot" -type "string" "zxy";
	setAttr ".jo" -type "double3" -2.0273227005001342 0 0 ;
	setAttr ".radi" 0.64046713209908512;
createNode joint -n "LatticeMiddle_01_LatticeLOC" -p "Facial_LatticeLoc_GRP";
	rename -uid "F92665DC-4AAB-B7AB-C480-8DAD56004091";
	setAttr ".t" -type "double3" -1.9721522630525286e-031 6 3.5761613052019792 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jot" -type "string" "yxz";
	setAttr ".radi" 0.55172413793103448;
createNode joint -n "LatticeUpper_00_LatticeLOC" -p "LatticeMiddle_01_LatticeLOC";
	rename -uid "DE4B680B-466C-8ECB-3E48-9CA125750ACF";
	setAttr ".t" -type "double3" -8.6281661508548166e-031 6 -2.2204460492503131e-015 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jot" -type "string" "yxz";
	setAttr ".radi" 0.55172413793103448;
createNode joint -n "LatticeLower_00_LatticeLOC" -p "LatticeMiddle_01_LatticeLOC";
	rename -uid "E7C5906C-4668-5F0E-9E26-88B4A1B79D50";
	setAttr ".t" -type "double3" 1.9721522630525286e-031 -6 -8.8817841970012523e-016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jot" -type "string" "yxz";
	setAttr ".radi" 0.55172413793103459;
createNode transform -n "HelpNodes_GRP" -p "Facial_Skeleton_GRP";
	rename -uid "FE07C1E7-4753-20DB-8D17-1AA10F07B65C";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
createNode transform -n "CVShapes" -p "HelpNodes_GRP";
	rename -uid "540F812B-4F64-7B2B-610E-1B8F1BBD34BF";
	setAttr -l on ".v" no;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "Eye_CV" -p "CVShapes";
	rename -uid "DD901382-4BC4-7079-CEB3-A2A1916954F7";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 2.8738811681459913 8.8173221255658127 5.7122009164108185 ;
createNode nurbsCurve -n "Eye_CVShape" -p "Eye_CV";
	rename -uid "5F294463-4F1D-58DF-7ED9-A5AE577D4A26";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 4;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		1.9801407923963061 1.4945788641414219 -0.5464575999899326
		1.9801407923963061 1.4945788641414219 3.3745085045806671
		-1.9647871431888992 1.4945788641414119 3.3745085045806671
		-1.9647871431888992 1.4945788641414119 -0.5464575999899326
		1.9801407923963061 1.4945788641414219 -0.5464575999899326
		1.9801407923963061 -1.1809970464677528 -0.54644353257495437
		1.9801407923963061 -1.1809970464677528 3.3745225719956435
		1.9801407923963061 1.4945788641414219 3.3745085045806671
		-1.9647871431888992 1.4945788641414119 3.3745085045806671
		-1.9647871431888992 -1.1809970464677628 3.3745225719956435
		-1.9647871431888992 -1.1809970464677628 -0.54644353257495437
		-1.9647871431888992 1.4945788641414119 -0.5464575999899326
		-1.9647871431888992 -1.1809970464677628 -0.54644353257495437
		1.9801407923963061 -1.1809970464677528 -0.54644353257495437
		1.9801407923963061 -1.1809970464677528 3.3745225719956435
		-1.9647871431888992 -1.1809970464677628 3.3745225719956435
		-1.9647871431888992 -1.1809970464677628 -0.54644353257495437
		;
createNode transform -n "Jaw_CV" -p "CVShapes";
	rename -uid "F840D718-406F-E651-C8E0-66B6A7152E7B";
	addAttr -ci true -sn "shapeType" -ln "shapeType" -dt "string";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 5.6716527584285696 1.8609980322317961 ;
	setAttr ".r" -type "double3" 41.235040530762099 0 0 ;
	setAttr ".s" -type "double3" 1.0000000000000002 0.99999999999999989 0.99999999999999989 ;
	setAttr ".shapeType" -type "string" "Jaw";
createNode nurbsCurve -n "Jaw_CVShape" -p "Jaw_CV";
	rename -uid "650CC6CD-4D35-7BA5-3F58-679F2D007263";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 9 0 no 3
		10 0 1 2 3 4 5 6 7 8 9
		10
		0 -0.032633684768407889 0.1689108123832308
		1.0110595542188927e-031 -0.0056706867178561993 8.2738131029790658
		-0.64856991308145784 0.013546098267388729 8.9220982619402456
		1.1687147348569591e-031 0.032762883252642538 9.5703834209014218
		0.64856991308145784 0.013546098267388729 8.9220982619402456
		1.0110595542188927e-031 -0.0056706867178561993 8.2738131029790658
		1.8888366429074846e-032 -0.63473906069378572 8.9413150469254923
		1.1687147348569591e-031 0.032762883252642538 9.5703834209014218
		1.9797062206933192e-031 0.65378391518885248 8.9031200201940912
		1.0110595542188927e-031 -0.0056706867178561993 8.2738131029790658
		;
createNode transform -n "HeadUpper_CV" -p "CVShapes";
	rename -uid "EA10560D-47F1-43DE-7047-88BB244D5EFA";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 7.8181383850397852 0 ;
createNode nurbsCurve -n "HeadUpper_CVShape" -p "HeadUpper_CV";
	rename -uid "AF4DC81A-4DB4-A5F5-1CFF-B5B15ADB6A7B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr ".cc" -type "nurbsCurve" 
		3 39 0 no 3
		44 0 0 0 1 2 3 6 6 6 9 9 9 12 12 12 13 14 15 16 17 18 19 20 21 22 23 24 25
		 26 27 28 29 30 31 32 33 36 36 36 37 38 39 39 39
		42
		6.7471770135387361 0.97149275973113469 -3.5325276894318209
		6.7471762075219051 0.97149325577017542 -3.5325286480230136
		6.747175401804256 0.97149375181633102 -3.5325296082135291
		6.747174595787409 0.97149424786248528 -3.5325305684040376
		7.0669785865552948 1.1648182209343343 -3.1495979163116576
		7.3001595026151644 1.361262013649283 -2.7604855861418307
		7.450457792928777 1.5634390585661353 -2.3600169262625732
		7.4739067714726257 1.477536569694941 -2.3604700803980485
		7.4973557500045391 1.391634073812769 -2.3609232345705085
		7.5208047285513775 1.3057315769290354 -2.3613763887482491
		7.8641988844605164 1.3029651387396861 -1.7385663399196074
		8.0798934161327391 1.3001915039883347 -1.1141361243531573
		8.1603502728635657 1.2973112475348894 -0.46570209488027525
		8.1603502728635657 1.2924959765031163 0.61836303911659252
		8.0798934161327391 1.2896157200447034 1.2667970697089939
		7.8641988844605164 1.2868420852933431 1.8912272852754468
		7.5208047285513775 1.2840756471039978 2.5140373341040867
		7.4973557500045391 1.3699781439877243 2.5144904882818269
		7.4739067714726257 1.4558806398699098 2.5149436424542864
		7.450457792928777 1.5417831287410986 2.5153967965897612
		7.3001595026151644 1.3360579862159783 2.9137136845525418
		7.0669785865552948 1.1361667114224738 3.3007352618555359
		6.747174595787409 0.93945000738247308 3.6816103637471396
		7.0669789336152551 0.74612604125055526 3.2986777276848347
		7.3001601881184257 0.54968224555931289 2.9095653911019195
		7.4504588133030198 0.34750519266543567 2.5090967231838515
		7.4739054891519148 0.43339687562595924 2.5095498203158177
		7.4973521649948278 0.51928855858647238 2.5100029174477871
		7.5207988408586806 0.60518024254855862 2.510456014585039
		7.8641931442084747 0.60794668127069118 1.8876458458081373
		8.0798865081436091 0.61071357607791321 1.263215684090562
		8.1603444302886405 0.6136005719476646 0.61478171959754591
		8.1603444302886405 0.61841584297945451 -0.46928341439932203
		8.0798865081436091 0.62128935975798727 -1.1177174506371843
		7.8641931442084747 0.62406973365145602 -1.7421475394903958
		7.5207988408586806 0.62683617237360312 -2.3649577082672977
		7.4973521649948278 0.54094448841151177 -2.3654108054045526
		7.4739054891519148 0.45505280545099958 -2.3658639025365154
		7.4504588133030198 0.36916112249047706 -2.3663169996684874
		7.3001605703032428 0.5748857497549662 -2.7646328859590774
		7.0669801172094067 0.7747765325440984 -3.1516535110469786
		6.7471770135387361 0.97149275973113469 -3.5325276894318209
		;
createNode nurbsCurve -n "HeadUpper_CVShape1" -p "HeadUpper_CV";
	rename -uid "A59A879A-4AFE-9F88-9245-A1A7034DEE14";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr ".cc" -type "nurbsCurve" 
		3 39 0 no 3
		44 0 0 0 1 2 3 6 6 6 9 9 9 12 12 12 13 14 15 16 17 18 19 20 21 22 23 24 25
		 26 27 28 29 30 31 32 33 36 36 36 37 38 39 39 39
		42
		-6.7471770135387361 0.97149275973113469 -3.5325276894318209
		-6.7471762075219051 0.97149325577017542 -3.5325286480230136
		-6.747175401804256 0.97149375181633102 -3.5325296082135291
		-6.747174595787409 0.97149424786248528 -3.5325305684040376
		-7.0669785865552948 1.1648182209343343 -3.1495979163116576
		-7.3001595026151644 1.361262013649283 -2.7604855861418307
		-7.450457792928777 1.5634390585661353 -2.3600169262625732
		-7.4739067714726284 1.477536569694941 -2.3604700803980485
		-7.4973557500045436 1.391634073812769 -2.3609232345705085
		-7.5208047285513775 1.3057315769290354 -2.3613763887482491
		-7.8641988844605262 1.3029651387396861 -1.7385663399196074
		-8.0798934161327391 1.3001915039883347 -1.1141361243531573
		-8.1603502728635657 1.2973112475348894 -0.46570209488027525
		-8.1603502728635657 1.2924959765031163 0.61836303911659252
		-8.0798934161327391 1.2896157200447034 1.2667970697089939
		-7.8641988844605262 1.2868420852933431 1.8912272852754468
		-7.5208047285513775 1.2840756471039978 2.5140373341040867
		-7.4973557500045436 1.3699781439877243 2.5144904882818269
		-7.4739067714726284 1.4558806398699098 2.5149436424542864
		-7.450457792928777 1.5417831287410986 2.5153967965897612
		-7.3001595026151644 1.3360579862159783 2.9137136845525418
		-7.0669785865552948 1.1361667114224738 3.3007352618555359
		-6.747174595787409 0.93945000738247308 3.6816103637471396
		-7.0669789336152631 0.74612604125055526 3.2986777276848347
		-7.3001601881184257 0.54968224555931289 2.9095653911019195
		-7.4504588133030198 0.34750519266543567 2.5090967231838515
		-7.4739054891519148 0.43339687562595924 2.5095498203158177
		-7.4973521649948278 0.51928855858647238 2.5100029174477871
		-7.5207988408586806 0.60518024254855862 2.510456014585039
		-7.8641931442084747 0.60794668127069118 1.8876458458081373
		-8.0798865081436091 0.61071357607791321 1.263215684090562
		-8.1603444302886405 0.6136005719476646 0.61478171959754591
		-8.1603444302886405 0.61841584297945451 -0.46928341439932203
		-8.0798865081436091 0.62128935975798727 -1.1177174506371843
		-7.8641931442084747 0.62406973365145602 -1.7421475394903958
		-7.5207988408586806 0.62683617237360312 -2.3649577082672977
		-7.4973521649948278 0.54094448841151177 -2.3654108054045526
		-7.4739054891519148 0.45505280545099958 -2.3658639025365154
		-7.4504588133030198 0.36916112249047706 -2.3663169996684874
		-7.3001605703032428 0.5748857497549662 -2.7646328859590774
		-7.0669801172094067 0.7747765325440984 -3.1516535110469786
		-6.7471770135387361 0.97149275973113469 -3.5325276894318209
		;
createNode transform -n "Head_CV" -p "CVShapes";
	rename -uid "A8FA2E24-48BC-E894-A11B-D4A79EE61B65";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 6.7213108154266488 0 ;
createNode nurbsCurve -n "Head_CVShape" -p "Head_CV";
	rename -uid "9EEFC5E6-4DD4-6E90-047B-C39EF0A96731";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		-1 1 0
		-1 3 0
		-2 3 0
		0 5 0
		2 3 0
		1 3 0
		1 1 0
		3 1 0
		3 2 0
		5 0 0
		3 -2 0
		3 -1 0
		1 -1 0
		1 -3 0
		2 -3 0
		0 -5 0
		-2 -3 0
		-1 -3 0
		-1 -1 0
		-3 -1 0
		-3 -2 0
		-5 0 0
		-3 2 0
		-3 1 0
		-1 1 0
		;
createNode transform -n "Teeth_CV" -p "CVShapes";
	rename -uid "838DD838-4682-E73C-2114-C1968B0EEA75";
createNode nurbsCurve -n "Teeth_CVShape" -p "Teeth_CV";
	rename -uid "D2AE9153-40E6-4249-9214-93A5A347C39F";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 12 2 no 3
		17 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		1.1982297340510875 5.5507632834890673e-017 -1.6932311384373948
		0.010237221973656565 6.4094693518606145e-017 -1.6932341631014511
		-1.2332879592246637 5.550763283489071e-017 -1.6932311384373948
		-1.2332940280688258 3.2047346759303085e-017 -1.6932228749015192
		-1.2332962494199617 2.1079388247500275e-032 1.5136026526239485e-006
		-1.2332940280688258 -3.204734675930306e-017 1.69323154615035
		-1.2332879592246637 -5.5507632834890697e-017 1.6932315462329859
		0.01023722197365599 -6.4094693518606133e-017 1.6932315462632319
		1.1982297340510875 -5.550763283489074e-017 1.6932315462329863
		1.1982369135597117 -3.2047346759303109e-017 1.6932315461503498
		1.198236913581926 -6.04338807272989e-032 1.5136026554951327e-006
		1.1982369135597117 3.2047346759303023e-017 -1.6932228749015197
		1.1982297340510875 5.5507632834890673e-017 -1.6932311384373948
		0.010237221973656565 6.4094693518606145e-017 -1.6932341631014511
		-1.2332879592246637 5.550763283489071e-017 -1.6932311384373948
		;
createNode transform -n "Lattice_CV" -p "CVShapes";
	rename -uid "63DEF77F-40A7-6C48-98EF-4A805E1E8630";
createNode nurbsCurve -n "Lattice_CVShape" -p "Lattice_CV";
	rename -uid "D518B1F1-42EB-D871-3282-8E861AFF4BE5";
	setAttr -k off ".v";
	setAttr ".tw" yes;
	setAttr -s 11 ".cp[0:10]" -type "double3" 5.1847920173001558 3.1747694741156794e-016 
		-5.1847920173001389 -8.365395300246711e-016 4.489802047702499e-016 -7.3324031889496233 
		-5.1847920173001452 3.1747694741156849e-016 -5.1847920173001452 -7.3324031889496233 
		1.8786157569091362e-031 -3.1652288450251313e-015 -5.1847920173001452 -3.1747694741156834e-016 
		5.1847920173001434 -2.2093961808789199e-015 -4.4898020477025029e-016 7.3324031889496304 
		5.1847920173001389 -3.1747694741156844e-016 5.1847920173001469 7.3324031889496233 
		-1.8338979887692122e-031 2.8977662132449656e-015 0 0 0 0 0 0 0 0 0;
createNode nurbsCurve -n "Lattice_CVShape1" -p "Lattice_CV";
	rename -uid "15C38198-4C81-EF9C-65FC-9D823CB27337";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		5.0493974054828401 3.0918641851237434e-016 -5.049397405482825
		-8.1469430565316228e-016 4.3725562636176421e-016 -7.1409262926453367
		-5.0493974054828303 3.0918641851237489e-016 -5.0493974054828303
		-7.1409262926453367 1.7760748717733632e-031 -2.9862261237452898e-015
		-5.0493974054828303 -3.0918641851237469e-016 5.0493974054828286
		-2.1517004551366695e-015 -4.3725562636176451e-016 7.140926292645343
		5.049397405482825 -3.0918641851237484e-016 5.0493974054828312
		7.1409262926453367 -1.8394910395877441e-031 2.9184411058239281e-015
		5.0493974054828401 3.0918641851237434e-016 -5.049397405482825
		-8.1469430565316228e-016 4.3725562636176421e-016 -7.1409262926453367
		-5.0493974054828303 3.0918641851237489e-016 -5.0493974054828303
		;
createNode transform -n "HelpCurves" -p "HelpNodes_GRP";
	rename -uid "97B04AC5-4472-92A9-D5AC-56A7C1D27489";
	setAttr -l on ".v";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "Brow_cv" -p "HelpCurves";
	rename -uid "E13133DE-4D9B-9E88-1A06-458855845224";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "Brow_cvShape" -p "Brow_cv";
	rename -uid "DDCAE450-459B-6411-C7AB-28A3A348A48F";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "Brow_cvShapeOrig" -p "Brow_cv";
	rename -uid "00CE86FF-4523-3B96-464F-06896008A843";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 8 0 no 3
		9 0 1 2 3 4 5 6 7 8
		9
		-5.8503628894613122 10.3752855238635 5.9211162469652514
		-4.7354907989501953 10.53758430480957 7.5964393615722656
		-3.2037782669067383 10.572027206420898 8.592747688293457
		-1.4691572189331055 10.356332568764975 9.0161819458007812
		0 10.382339477539062 9.1043643951416016
		1.4691572189331055 10.356332568764975 9.0161819458007812
		3.2037782669067383 10.572027206420898 8.592747688293457
		4.7354907989501953 10.53758430480957 7.5964393615722656
		5.8503628894613122 10.3752855238635 5.9211162469652514
		;
createNode transform -n "L_Socket_cv" -p "HelpCurves";
	rename -uid "0E1DFCB5-4CAC-AAF9-9C34-149708EF8A87";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "L_Socket_cvShape" -p "L_Socket_cv";
	rename -uid "53D88FA4-47C9-0B44-5A8B-09928F390F96";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "L_Socket_cvShapeOrig" -p "L_Socket_cv";
	rename -uid "FE696A8E-43ED-9980-940A-27BC6FFA86C4";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 8 0 no 3
		9 0 1 2 3 4 5 6 7 8
		9
		1.3782232003889379 8.2179290344994254 8.058346524499667
		1.9497871398925781 9.4036388397216797 8.280426025390625
		3.3550353050231934 9.7519245147705078 8.0734004974365234
		4.6270670890808105 9.7465419769287109 7.1343746185302734
		5.0318503379821777 9.2830460438015887 6.3610515594482422
		4.6187248229980469 8.0747470855712891 6.7844409942626953
		3.2839744577947449 7.4680519104003906 7.6035885810852051
		2.0820850144959206 7.7015838623046875 7.840672492980957
		1.3782232003889379 8.2179290344994254 8.058346524499667
		;
createNode transform -n "L_Lid_cv" -p "HelpCurves";
	rename -uid "AFA2DE79-4D84-B156-A8DC-42BBEF54B1E8";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "L_Lid_cvShape" -p "L_Lid_cv";
	rename -uid "D97A912D-4D12-B6C9-5A4D-3CA908F3A239";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "L_Lid_cvShapeOrig" -p "L_Lid_cv";
	rename -uid "12BB59FF-4940-4550-FB20-92A68F5231FB";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 8 0 no 3
		9 0 1 2 3 4 5 6 7 8
		9
		1.6553013324737549 8.2814254760742187 7.8856148719787598
		2.0917415618896484 8.4562473297119141 8.0394248962402344
		3.3179900646209717 8.7515964508056641 7.9887332916259766
		4.4987268447875977 9.1129188537597656 7.1400823593139648
		4.8247900009155273 9.2105464935302734 6.5966176986694336
		4.514655590057373 8.8801898956298828 7.0841550827026367
		3.3083300590515137 8.4016151428222656 7.9009857177734375
		2.0934193134307861 8.2320842742919922 7.9774303436279297
		1.6553013324737549 8.2814254760742187 7.8856148719787598
		;
createNode transform -n "R_Socket_cv" -p "HelpCurves";
	rename -uid "07563423-4725-8FC2-D154-49B49ACCD8DA";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "R_Socket_cvShape" -p "R_Socket_cv";
	rename -uid "6D0AAB55-47A2-260D-20BC-4B90AEFE9741";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "R_Socket_cvShapeOrig" -p "R_Socket_cv";
	rename -uid "C0876068-4E04-3461-A0A3-BCBEC79F5B8F";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 8 0 no 3
		9 0 1 2 3 4 5 6 7 8
		9
		-1.3782232003889379 8.2179290344994254 8.058346524499667
		-1.9497871398925781 9.4036388397216797 8.280426025390625
		-3.3550353050231934 9.7519245147705078 8.0734004974365234
		-4.6270670890808105 9.7465419769287109 7.1343746185302734
		-5.0318503379821777 9.2830460438015887 6.3610515594482422
		-4.6187248229980469 8.0747470855712891 6.7844409942626953
		-3.2839744577947449 7.4680519104003906 7.6035885810852051
		-2.0820850144959206 7.7015838623046875 7.840672492980957
		-1.3782232003889379 8.2179290344994254 8.058346524499667
		;
createNode transform -n "R_Lid_cv" -p "HelpCurves";
	rename -uid "2A655B2C-412B-594D-9AB0-F09BAFC8B504";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "R_Lid_cvShape" -p "R_Lid_cv";
	rename -uid "657C8BB0-45B1-9E63-53DD-F49BFF14686D";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "R_Lid_cvShapeOrig" -p "R_Lid_cv";
	rename -uid "E486C7E8-490A-D746-5528-F29948DCB4A5";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 8 0 no 3
		9 0 1 2 3 4 5 6 7 8
		9
		-1.6553013324737549 8.2814254760742187 7.8856148719787598
		-2.0917415618896484 8.4562473297119141 8.0394248962402344
		-3.3179900646209717 8.7515964508056641 7.9887332916259766
		-4.4987268447875977 9.1129188537597656 7.1400823593139648
		-4.8247900009155273 9.2105464935302734 6.5966176986694336
		-4.514655590057373 8.8801898956298828 7.0841550827026367
		-3.3083300590515137 8.4016151428222656 7.9009857177734375
		-2.0934193134307861 8.2320842742919922 7.9774303436279297
		-1.6553013324737549 8.2814254760742187 7.8856148719787598
		;
createNode transform -n "L_Orbit_cv" -p "HelpCurves";
	rename -uid "1174460C-4D44-1321-1650-C3948A4A8B9B";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "L_Orbit_cvShape" -p "L_Orbit_cv";
	rename -uid "8342CF66-468E-1183-E43F-598C595A631B";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "L_Orbit_cvShapeOrig" -p "L_Orbit_cv";
	rename -uid "8C6FE42C-4CF0-C880-4D79-489F6DFB0AED";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		1.5547847747802734 7.1849288940429687 8.1608667373657227
		2.9833431243896484 6.4433689117431641 7.890528678894043
		4.4723429679870605 6.6044464111328125 6.7346591949462891
		5.333162784576416 7.5637702941894531 5.7535190582275391
		;
createNode transform -n "R_Orbit_cv" -p "HelpCurves";
	rename -uid "A343A037-4788-0255-1F72-90B85B3C9EDD";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "R_Orbit_cvShape" -p "R_Orbit_cv";
	rename -uid "B71A3B89-41F5-BB0D-EBBC-4F85AB2B8D8C";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "R_Orbit_cvShapeOrig" -p "R_Orbit_cv";
	rename -uid "0A177B9A-4C9C-0E17-45C2-2D89FD000C2D";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 3 0 no 3
		4 0 1 2 3
		4
		-1.5547847747802734 7.1849288940429687 8.1608667373657227
		-2.9833431243896484 6.4433689117431641 7.890528678894043
		-4.4723429679870605 6.6044464111328125 6.7346591949462891
		-5.333162784576416 7.5637702941894531 5.7535190582275391
		;
createNode transform -n "Mouth_cv" -p "HelpCurves";
	rename -uid "DD1B08CB-4858-BFAC-86E9-1191EBBB1B85";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "Mouth_cvShape" -p "Mouth_cv";
	rename -uid "1CE6DCC3-4564-E365-D442-F3A466FDBF3C";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "Mouth_cvShapeOrig" -p "Mouth_cv";
	rename -uid "FD7A47FF-4DF0-8F78-0ECE-89A12C2BA7B3";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 10 0 no 3
		11 0 1 2 3 4 5 6 7 8 9 10
		11
		-1.2832523584365845 6.3339557647705078 8.5894432067871094
		-2.1263527870178223 5.1193389892578125 8.1643352508544922
		-2.3640142343991828 3.9333019256591797 7.6348066329956064
		-2.0158705354273443 2.7136820426164658 7.1741893847108393
		-1.1348832059433636 2.0061206817626953 7.3398809432983398
		0 1.8350624279599814 7.6724090284968298
		1.1348832059433636 2.0061206817626953 7.3398809432983398
		2.0158705354273443 2.7136820426164658 7.1741893847108393
		2.3640142343991828 3.9333019256591797 7.6348066329956064
		2.1263527870178223 5.1193389892578125 8.1643352508544922
		1.2832523584365845 6.3339557647705078 8.5894432067871094
		;
createNode transform -n "Lip_cv" -p "HelpCurves";
	rename -uid "323A51E8-4B28-EE6A-D2A5-51A43F1F9376";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "Lip_cvShape" -p "Lip_cv";
	rename -uid "3327C61D-4408-5EED-7695-7C9833CE9ADA";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "Lip_cvShapeOrig" -p "Lip_cv";
	rename -uid "DEC58447-4743-FB40-D140-EA9A3B4B1049";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-1.6381075382232666 3.789484977722168 7.848480224609375
		-1.4180364608764648 3.9101667404174805 8.1984710693359375
		-1.0074524879455566 4.0015859603881836 8.5875701904296875
		-0.54260778427124023 4.028529167175293 8.8784980773925781
		0 4.0269913673400879 8.9925823211669922
		0.54260778427124023 4.028529167175293 8.8784980773925781
		1.0074524879455566 4.0015859603881836 8.5875701904296875
		1.4180364608764648 3.9101667404174805 8.1984710693359375
		1.6381075382232666 3.789484977722168 7.848480224609375
		1.4596633911132812 3.6742439270019531 8.0475120544433594
		1.0965092182159424 3.5773906707763672 8.4012517929077148
		0.61316394805908203 3.5082130432128906 8.7187004089355469
		0 3.4986839294433594 8.8420066833496094
		-0.61316394805908203 3.5082130432128906 8.7187004089355469
		-1.0965092182159424 3.5773906707763672 8.4012517929077148
		-1.4596633911132812 3.6742439270019531 8.0475120544433594
		-1.6381075382232666 3.789484977722168 7.848480224609375
		;
createNode transform -n "JawLine_cv" -p "HelpCurves";
	rename -uid "9C979FB4-48E4-DB2E-7EC4-20A508231695";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "JawLine_cvShape" -p "JawLine_cv";
	rename -uid "A06C0B98-4A71-8E88-2E31-57936AC0802A";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "JawLine_cvShapeOrig" -p "JawLine_cv";
	rename -uid "B5E982BB-407F-153B-BE4E-23A717DAD142";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 6 0 no 3
		7 0 1 2 3 4 5 6
		7
		-4.6366920471191406 3.0374965667724609 2.3502998352050781
		-3.6291710926439311 2.1692889871743195 4.0004947173865943
		-1.9805426546013161 1.1638710466391315 5.602295934346035
		0 0.58954048156738281 7.0004043579101563
		1.9805426546013161 1.1638710466391315 5.602295934346035
		3.6291710926439311 2.1692889871743195 4.0004947173865943
		4.6366920471191406 3.0374965667724609 2.3502998352050781
		;
createNode transform -n "TeethUpper_cv" -p "HelpCurves";
	rename -uid "B8CA217D-42D9-40D4-63E3-009113748806";
	setAttr -l on ".v" no;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "TeethUpper_cvShape" -p "TeethUpper_cv";
	rename -uid "65969025-4DC0-D47F-326A-DD9CE2FAA034";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "TeethUpper_cvShapeOrig" -p "TeethUpper_cv";
	rename -uid "AD4819A6-4E54-A9D9-B61B-FE844909BAA1";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 6 0 no 3
		7 0 1 2 3 4 5 6
		7
		-1.6675544373762092 5.0937881391219291 6.1171743166102139
		-1.6675544373762092 4.9882382240685503 6.5727718476563508
		-1.2062406368665213 4.7159946563617536 7.7478888264590697
		0 4.6118780223795106 8.1972997175920046
		1.2062406368665213 4.7159946563617536 7.7478888264590688
		1.6675544373762092 4.9882382240685503 6.5727718476563508
		1.6675544373762092 5.0937881391219282 6.1171743166102139
		;
createNode transform -n "TeethLower_cv" -p "HelpCurves";
	rename -uid "4E531A4E-4F94-9532-56B8-EFBEE0B8ED8B";
	setAttr -l on ".v" no;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "TeethLower_cvShape" -p "TeethLower_cv";
	rename -uid "263CE97E-4E37-738C-B2DF-9E83CA66DD06";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "TeethLower_cvShapeOrig" -p "TeethLower_cv";
	rename -uid "35E2DEC6-4A29-E70B-5D9D-D6A67B096740";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 6 0 no 3
		7 0 1 2 3 4 5 6
		7
		-1.6675544373762095 3.9491887676111115 5.8275263648530657
		-1.6675544373762095 3.7129115380178344 6.761221103083181
		-1.0546792475043469 3.5014509711048429 7.5968480444083664
		0 3.4199367585495035 7.9189670716413518
		1.0546792475043469 3.501450971104842 7.5968480444083664
		1.6675544373762095 3.7129115380178335 6.7612211030831801
		1.6675544373762095 3.9491887676111106 5.8275263648530657
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "E54BEB9E-41B0-AAAE-B9F7-1CBE2231C696";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "C5D68390-4C04-0BCD-9AC5-4982F6455984";
createNode displayLayer -n "defaultLayer";
	rename -uid "D0CA154C-48E1-48E3-862C-279DF4B49D8B";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "7C5AE4E3-4DFE-BF1E-A8C5-C1A94CE958A1";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "158246A0-4244-23C2-B1B5-BFBA5C09753F";
	setAttr ".g" yes;
createNode ilrOptionsNode -s -n "TurtleRenderOptions";
	rename -uid "331AA930-498C-AE84-A91D-DEB9DB0420D3";
lockNode -l 1 ;
createNode ilrUIOptionsNode -s -n "TurtleUIOptions";
	rename -uid "4754D2B1-403A-FE58-8227-15B9591E1084";
lockNode -l 1 ;
createNode ilrBakeLayerManager -s -n "TurtleBakeLayerManager";
	rename -uid "0999AE1D-4305-0F28-600E-5C88727321BA";
lockNode -l 1 ;
createNode ilrBakeLayer -s -n "TurtleDefaultBakeLayer";
	rename -uid "06915C3A-4FDE-DA6D-6D25-C38CF7484758";
lockNode -l 1 ;
createNode groupId -n "skinCluster1GroupId";
	rename -uid "7D528D47-4426-56EF-DD12-BE83B9644660";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster1Set";
	rename -uid "BB7F4F5E-4FCA-E8AB-6A96-AA95E3ADCDEA";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster1";
	rename -uid "5801A3BC-4E58-11D6-3A63-E3BF511452FA";
	setAttr -s 9 ".wl";
	setAttr ".wl[0].w[29]"  1;
	setAttr ".wl[1].w[28]"  1;
	setAttr ".wl[2].w[27]"  1;
	setAttr ".wl[3].w[26]"  1;
	setAttr ".wl[4].w[0]"  1;
	setAttr ".wl[5].w[1]"  1;
	setAttr ".wl[6].w[2]"  1;
	setAttr ".wl[7].w[3]"  1;
	setAttr ".wl[8].w[4]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 9 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 9 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 9 ".ifcl";
createNode groupParts -n "skinCluster1GroupParts";
	rename -uid "0A2CF2FA-44F3-E38D-19C9-CBAC831B80F6";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster3GroupId";
	rename -uid "8A5ADFCB-4C8B-BC4A-5797-A098C5FA9E7E";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster3Set";
	rename -uid "70E9D6DE-4F45-55D5-AE99-95A67FDBC82F";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster3";
	rename -uid "EE57C88A-4E26-1E78-5123-D0AEB0E3FCD8";
	setAttr -s 9 ".wl";
	setAttr ".wl[0].w[6]"  1;
	setAttr ".wl[1].w[7]"  1;
	setAttr ".wl[2].w[8]"  1;
	setAttr ".wl[3].w[9]"  1;
	setAttr ".wl[4].w[10]"  1;
	setAttr ".wl[5].w[13]"  1;
	setAttr ".wl[6].w[12]"  1;
	setAttr ".wl[7].w[11]"  1;
	setAttr ".wl[8].w[6]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 8 ".lw";
	setAttr -s 8 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 8 ".ifcl";
	setAttr -s 8 ".ifcl";
createNode groupParts -n "skinCluster3GroupParts";
	rename -uid "DE00709D-457C-DF66-0E4A-858D710F69EB";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster2GroupId";
	rename -uid "C3360397-4DBD-F657-DA2A-8DB697DA6FBD";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster2Set";
	rename -uid "2EFD3BAE-4023-0387-03F5-7FBFF81FF826";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster2";
	rename -uid "BD6443BC-4CDA-8D8C-D3FE-81A1A637720D";
	setAttr -s 9 ".wl";
	setAttr ".wl[0].w[14]"  1;
	setAttr ".wl[1].w[15]"  1;
	setAttr ".wl[2].w[16]"  1;
	setAttr ".wl[3].w[17]"  1;
	setAttr ".wl[4].w[18]"  1;
	setAttr ".wl[5].w[21]"  1;
	setAttr ".wl[6].w[20]"  1;
	setAttr ".wl[7].w[19]"  1;
	setAttr ".wl[8].w[14]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 8 ".lw";
	setAttr -s 8 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 8 ".ifcl";
	setAttr -s 8 ".ifcl";
createNode groupParts -n "skinCluster2GroupParts";
	rename -uid "CE7658F2-4FDF-96F9-2C3E-5A98BE4C8622";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster4GroupId";
	rename -uid "0246D0DE-4059-AB73-0319-7885D456C59B";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster4Set";
	rename -uid "8A841EA9-41F2-A276-F43E-7F92AD359A19";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster4";
	rename -uid "F117BEFB-4689-F833-A4D0-CDBB85DE1C66";
	setAttr -s 9 ".wl";
	setAttr ".wl[0].w[42]"  1;
	setAttr ".wl[1].w[47]"  1;
	setAttr ".wl[2].w[48]"  1;
	setAttr ".wl[3].w[49]"  1;
	setAttr ".wl[4].w[46]"  1;
	setAttr ".wl[5].w[45]"  1;
	setAttr ".wl[6].w[44]"  1;
	setAttr ".wl[7].w[43]"  1;
	setAttr ".wl[8].w[42]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 8 ".lw";
	setAttr -s 8 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 8 ".ifcl";
	setAttr -s 8 ".ifcl";
createNode groupParts -n "skinCluster4GroupParts";
	rename -uid "45684342-41CD-6D56-968D-C99B5FCE9FC4";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster5GroupId";
	rename -uid "5679E0F4-4582-C920-DD0E-1B9CDA4629AD";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster5Set";
	rename -uid "EAEEC7A6-4B6F-33BB-B58D-89A89B5DAE27";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster5";
	rename -uid "7D33D564-44DE-ECB6-4799-7BAF66EC6197";
	setAttr -s 9 ".wl";
	setAttr ".wl[0].w[30]"  1;
	setAttr ".wl[1].w[35]"  1;
	setAttr ".wl[2].w[36]"  1;
	setAttr ".wl[3].w[37]"  1;
	setAttr ".wl[4].w[34]"  1;
	setAttr ".wl[5].w[33]"  1;
	setAttr ".wl[6].w[32]"  1;
	setAttr ".wl[7].w[31]"  1;
	setAttr ".wl[8].w[30]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 8 ".lw";
	setAttr -s 8 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 8 ".ifcl";
	setAttr -s 8 ".ifcl";
createNode groupParts -n "skinCluster5GroupParts";
	rename -uid "7920925A-45DB-584B-163E-A2821429BF98";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster6GroupId";
	rename -uid "D3D1D4BA-47E3-690C-4B01-2D9CDEE42934";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster6Set";
	rename -uid "E8FD4DBB-4381-A009-157F-D098A4F2DE7D";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster6";
	rename -uid "718D9F82-4683-0ED1-43DD-A5975357E384";
	setAttr -s 4 ".wl";
	setAttr ".wl[0].w[22]"  1;
	setAttr ".wl[1].w[23]"  1;
	setAttr ".wl[2].w[24]"  1;
	setAttr ".wl[3].w[25]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 4 ".lw";
	setAttr -s 4 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 4 ".ifcl";
	setAttr -s 4 ".ifcl";
createNode groupParts -n "skinCluster6GroupParts";
	rename -uid "8388EA97-4095-C6E5-4F91-FE8A63B6A5E3";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster7GroupId";
	rename -uid "D391EC82-474A-149E-B625-51A7DFEBB9F0";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster7Set";
	rename -uid "7C9B978D-4879-A576-3D87-BEA86F75BD53";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster7";
	rename -uid "8247F2BF-487D-109A-89A1-1193181B015A";
	setAttr -s 4 ".wl";
	setAttr ".wl[0].w[38]"  1;
	setAttr ".wl[1].w[39]"  1;
	setAttr ".wl[2].w[40]"  1;
	setAttr ".wl[3].w[41]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 4 ".lw";
	setAttr -s 4 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 4 ".ifcl";
	setAttr -s 4 ".ifcl";
createNode groupParts -n "skinCluster7GroupParts";
	rename -uid "97474580-4860-C279-6972-919ACE74464C";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster8GroupId";
	rename -uid "E8FEE090-4BED-A7F0-990E-66A323974198";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster8Set";
	rename -uid "C9A155C2-41D6-F760-DFE5-E7B9AE20ACD0";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster8";
	rename -uid "ED24AC9A-47FE-81E4-78FF-F3A8AB48DA27";
	setAttr -s 11 ".wl";
	setAttr ".wl[0].w[51]"  1;
	setAttr ".wl[1].w[53]"  1;
	setAttr ".wl[2].w[74]"  1;
	setAttr ".wl[3].w[76]"  1;
	setAttr ".wl[4].w[75]"  1;
	setAttr ".wl[5].w[64]"  1;
	setAttr ".wl[6].w[65]"  1;
	setAttr ".wl[7].w[66]"  1;
	setAttr ".wl[8].w[63]"  1;
	setAttr ".wl[9].w[52]"  1;
	setAttr ".wl[10].w[50]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 11 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 11 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 11 ".ifcl";
createNode groupParts -n "skinCluster8GroupParts";
	rename -uid "41CC3D8C-4A7A-D6C1-9B5A-F3A4B689842C";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster9GroupId";
	rename -uid "E8AF0D09-4423-6871-65B1-6285261EA503";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster9Set";
	rename -uid "2725D569-420F-54F8-CF16-C18FADF55016";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster9";
	rename -uid "5B599166-4E9D-367A-9C10-F6BC5A966B01";
	setAttr -s 17 ".wl";
	setAttr ".wl[0].w[70]"  1;
	setAttr ".wl[1].w[73]"  1;
	setAttr ".wl[2].w[72]"  1;
	setAttr ".wl[3].w[71]"  1;
	setAttr ".wl[4].w[54]"  1;
	setAttr ".wl[5].w[55]"  1;
	setAttr ".wl[6].w[56]"  1;
	setAttr ".wl[7].w[57]"  1;
	setAttr ".wl[8].w[58]"  1;
	setAttr ".wl[9].w[62]"  1;
	setAttr ".wl[10].w[61]"  1;
	setAttr ".wl[11].w[60]"  1;
	setAttr ".wl[12].w[59]"  1;
	setAttr ".wl[13].w[67]"  1;
	setAttr ".wl[14].w[68]"  1;
	setAttr ".wl[15].w[69]"  1;
	setAttr ".wl[16].w[70]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 16 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 16 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 16 ".ifcl";
createNode groupParts -n "skinCluster9GroupParts";
	rename -uid "4F1B5B08-4A51-99F5-8D0A-F58E377A0623";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupId -n "skinCluster10GroupId";
	rename -uid "77FF18F4-4030-EBBB-4E7E-D19A5B74F4F3";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster10Set";
	rename -uid "91F785D1-48B5-5FD5-B602-079C3AA7FFD5";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "HelpNodes_skinCluster10";
	rename -uid "B567E6FC-465C-148F-F3A7-01894360B2AF";
	setAttr -s 7 ".wl";
	setAttr ".wl[0].w[82]"  1;
	setAttr ".wl[1].w[81]"  1;
	setAttr ".wl[2].w[80]"  1;
	setAttr ".wl[3].w[83]"  1;
	setAttr ".wl[4].w[79]"  1;
	setAttr ".wl[5].w[78]"  1;
	setAttr ".wl[6].w[77]"  1;
	setAttr -s 84 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -10.382339477539062 -9.1043643951416016 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -1.4691572189331057 -10.356332568764975 -9.0161819458007812 1;
	setAttr ".pm[2]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.2037782669067392 -10.572027206420898 -8.592747688293457 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7354907989501953 -10.537584304809569 -7.5964393615722665 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1.0000000000000002 0 -5.8503628894613122 -10.3752855238635 -5.9211162469652523 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -8.3340854644775391 -8.7626216251277107 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3782232003889379 -8.2179290344994254 -8.058346524499667 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9497871398925781 -9.4036388397216797 -8.280426025390625 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3550353050231934 -9.7519245147705078 -8.0734004974365234 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6270670890808105 -9.7465419769287109 -7.1343746185302734 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.0318503379821777 -9.2830460438015887 -6.3610515594482422 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0820850144959206 -7.7015838623046875 -7.840672492980957 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2839744577947449 -7.4680519104003906 -7.6035885810852051 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6187248229980469 -8.0747470855712891 -6.7844409942626953 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6553013324737549 -8.2814254760742187 -7.8856148719787598 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0917415618896484 -8.4562473297119141 -8.0394248962402344 1;
	setAttr ".pm[16]" -type "matrix" 1.0000000000000002 0 0 0 0 1 0 0 0 0 1 0 -3.3179900646209726 -8.7515964508056641 -7.9887332916259775 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4987268447875977 -9.1129188537597656 -7.1400823593139648 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.8247900009155273 -9.2105464935302734 -6.5966176986694336 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0934193134307861 -8.2320842742919922 -7.9774303436279297 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.3083300590515137 -8.4016151428222656 -7.9009857177734375 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.514655590057373 -8.8801898956298828 -7.0841550827026367 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5547847747802734 -7.1849288940429687 -8.1608667373657227 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.9833431243896484 -6.4433689117431641 -7.890528678894043 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.4723429679870597 -6.6044464111328134 -6.73465919494629 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1.0000000000000002 0 0 0 0 1.0000000000000002 0
		 -5.3331627845764169 -7.5637702941894558 -5.7535190582275408 1;
	setAttr ".pm[26]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -1.4691572189331046 -10.356332568764975 9.0161819458007812 1;
	setAttr ".pm[27]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.2037782669067383 -10.572027206420898 8.592747688293457 1;
	setAttr ".pm[28]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.7354907989501944 -10.537584304809569 7.5964393615722674 1;
	setAttr ".pm[29]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1.0000000000000002 0
		 -5.8503628894613113 -10.3752855238635 5.9211162469652532 1;
	setAttr ".pm[30]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.655301332473754 -8.2814254760742187 7.8856148719787598 1;
	setAttr ".pm[31]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0934193134307852 -8.2320842742919922 7.9774303436279297 1;
	setAttr ".pm[32]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3083300590515128 -8.4016151428222656 7.9009857177734375 1;
	setAttr ".pm[33]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.5146555900573722 -8.8801898956298828 7.0841550827026376 1;
	setAttr ".pm[34]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.8247900009155265 -9.2105464935302734 6.5966176986694345 1;
	setAttr ".pm[35]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0917415618896475 -8.4562473297119141 8.0394248962402344 1;
	setAttr ".pm[36]" -type "matrix" -1.0000000000000002 0 1.2246467991473532e-016 0
		 0 1 0 0 -1.2246467991473535e-016 0 -1 0 -3.3179900646209717 -8.7515964508056641 7.9887332916259775 1;
	setAttr ".pm[37]" -type "matrix" -1 0 1.224646799147353e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.4987268447875968 -9.1129188537597656 7.1400823593139657 1;
	setAttr ".pm[38]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.5547847747802723 -7.1849288940429687 8.1608667373657227 1;
	setAttr ".pm[39]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.9833431243896475 -6.4433689117431641 7.890528678894043 1;
	setAttr ".pm[40]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.224646799147353e-016 0 -1 0
		 -4.4723429679870588 -6.6044464111328134 6.7346591949462908 1;
	setAttr ".pm[41]" -type "matrix" -1 0 1.2246467991473535e-016 0 0 1.0000000000000002 0 0
		 -1.2246467991473532e-016 0 -1.0000000000000002 0 -5.333162784576416 -7.5637702941894558 5.7535190582275417 1;
	setAttr ".pm[42]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.378223200388937 -8.2179290344994254 8.058346524499667 1;
	setAttr ".pm[43]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0820850144959198 -7.7015838623046875 7.840672492980957 1;
	setAttr ".pm[44]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.2839744577947441 -7.4680519104003906 7.6035885810852051 1;
	setAttr ".pm[45]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.618724822998046 -8.0747470855712891 6.7844409942626962 1;
	setAttr ".pm[46]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -5.0318503379821768 -9.2830460438015887 6.3610515594482431 1;
	setAttr ".pm[47]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.949787139892577 -9.4036388397216797 8.280426025390625 1;
	setAttr ".pm[48]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.3550353050231925 -9.7519245147705078 8.0734004974365234 1;
	setAttr ".pm[49]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6270670890808097 -9.7465419769287109 7.1343746185302743 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2832523584365845 -6.3339557647705078 -8.5894432067871094 1;
	setAttr ".pm[51]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.2832523584365834 -6.3339557647705078 8.5894432067871094 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1263527870178223 -5.1193389892578125 -8.1643352508544922 1;
	setAttr ".pm[53]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.1263527870178214 -5.1193389892578125 8.1643352508544922 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4.0269913673400879 -8.9925823211669922 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.54260778427124023 -4.028529167175293 -8.8784980773925781 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0074524879455566 -4.0015859603881836 -8.5875701904296875 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4180364608764648 -3.9101667404174805 -8.1984710693359375 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6381075382232666 -3.789484977722168 -7.848480224609375 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -3.4986839294433594 -8.8420066833496094 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.61316394805908203 -3.5082130432128906 -8.7187004089355469 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0965092182159424 -3.5773906707763672 -8.4012517929077148 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4596633911132812 -3.6742439270019531 -8.0475120544433594 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3640142343991828 -3.9333019256591797 -7.6348066329956064 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.8350624279599814 -7.6724090284968298 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1348832059433636 -2.0061206817626953 -7.3398809432983398 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158705354273443 -2.7136820426164658 -7.1741893847108393 1;
	setAttr ".pm[67]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.61316394805908092 -3.5082130432128906 8.7187004089355469 1;
	setAttr ".pm[68]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0965092182159413 -3.5773906707763672 8.4012517929077148 1;
	setAttr ".pm[69]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4596633911132804 -3.6742439270019531 8.0475120544433594 1;
	setAttr ".pm[70]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.6381075382232657 -3.789484977722168 7.848480224609375 1;
	setAttr ".pm[71]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -0.54260778427123912 -4.028529167175293 8.8784980773925781 1;
	setAttr ".pm[72]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.0074524879455555 -4.0015859603881836 8.5875701904296875 1;
	setAttr ".pm[73]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.4180364608764637 -3.9101667404174805 8.1984710693359375 1;
	setAttr ".pm[74]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.3640142343991819 -3.9333019256591797 7.6348066329956064 1;
	setAttr ".pm[75]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.1348832059433627 -2.0061206817626953 7.3398809432983398 1;
	setAttr ".pm[76]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -2.0158705354273434 -2.7136820426164658 7.1741893847108393 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.6366920471191406 -3.0374965667724609 -2.3502998352050781 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6291710926439311 -2.1692889871743195 -4.0004947173865943 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9805426546013161 -1.1638710466391315 -5.602295934346035 1;
	setAttr ".pm[80]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -1.9805426546013154 -1.1638710466391315 5.602295934346035 1;
	setAttr ".pm[81]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -3.6291710926439307 -2.1692889871743195 4.0004947173865952 1;
	setAttr ".pm[82]" -type "matrix" -1 0 1.2246467991473532e-016 0 0 1 0 0 -1.2246467991473532e-016 0 -1 0
		 -4.6366920471191406 -3.0374965667724609 2.3502998352050786 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -0.58954048156738281 -7.0004043579101563 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 7 ".ma";
	setAttr -s 84 ".dpf[0:83]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 7 ".lw";
	setAttr -s 7 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 7 ".ifcl";
	setAttr -s 7 ".ifcl";
createNode groupParts -n "skinCluster10GroupParts";
	rename -uid "F1BA1F14-433A-E01B-40AA-C78F4F8B91B7";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "D489603C-407F-C491-4CC7-FE9D1B1AB8FE";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -docTag \"RADRENDER\" \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -docTag \"RADRENDER\" \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n"
		+ "                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n"
		+ "                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n"
		+ "                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n"
		+ "            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -docTag \"RADRENDER\" \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -docTag \"RADRENDER\" \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 1\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n"
		+ "                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n"
		+ "                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n"
		+ "                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 721\n                -height 849\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 1\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n"
		+ "            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 721\n            -height 849\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showReferenceNodes 1\n                -showReferenceMembers 1\n                -showAttributes 0\n"
		+ "                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n"
		+ "                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showReferenceNodes 1\n"
		+ "            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n"
		+ "            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n"
		+ "                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n"
		+ "                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n"
		+ "                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n"
		+ "                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n"
		+ "                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n"
		+ "                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n"
		+ "                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n"
		+ "                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n"
		+ "                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n"
		+ "                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n"
		+ "                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n"
		+ "                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n"
		+ "\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n"
		+ "                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n"
		+ "                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\tif ($useSceneConfig) {\n\t\tscriptedPanel -e -to $panelName;\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"profilerPanel\" -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"Stereo\" -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels `;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -editorChanged \"updateModelPanelBar\" \n"
		+ "                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n"
		+ "                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererOverrideName \"stereoOverrideVP2\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n"
		+ "                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n"
		+ "                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -editorChanged \"updateModelPanelBar\" \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererOverrideName \"stereoOverrideVP2\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n"
		+ "                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n"
		+ "                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n"
		+ "\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n"
		+ "                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n"
		+ "                -additiveGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n"
		+ "\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 28 100 -ps 2 72 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Outliner\")) \n\t\t\t\t\t\"outlinerPanel\"\n\t\t\t\t\t\"$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    $editorName\"\n"
		+ "\t\t\t\t\t\"outlinerPanel -edit -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 1\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 721\\n    -height 849\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 1\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 721\\n    -height 849\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "7D922A1C-4A35-493E-0C4A-1F9D06E7CFE6";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode ffd -n "Facial_LatticeFFD";
	rename -uid "55FDA23A-4D40-61E0-74EE-44964076D537";
	setAttr ".lo" yes;
createNode objectSet -n "Facial_LatticeSet";
	rename -uid "FE4E248C-4C8B-0AFE-3402-3480ED770306";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "334A95FC-4643-984E-4DCD-F6B0895BEB0A";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -443.75600393716894 -1645.2197943348165 ;
	setAttr ".tgi[0].vh" -type "double2" 2759.6052507487821 127.88939962828832 ;
createNode polyCube -n "polyCube1_Skin";
	rename -uid "E7A46E72-4C17-E9EA-45F6-66945827EBD6";
	setAttr ".cuv" 4;
createNode polyCube -n "polyCube1_Head_Lattice";
	rename -uid "EC027118-4A57-DC63-E9E3-C6843F6C8634";
	setAttr ".cuv" 4;
createNode polyCube -n "polyCube1_Jaw_Lattice";
	rename -uid "6132D450-4781-480E-7B3F-E69ED556B34E";
	setAttr ".cuv" 4;
createNode makeNurbCircle -n "makeNurbCircle1";
	rename -uid "B1390B57-4BFA-FF88-82AD-74A59C5A1868";
	setAttr ".nr" -type "double3" 0 1 0 ;
createNode transformGeometry -n "transformGeometry1";
	rename -uid "BA03CA49-4CC2-B6CA-251A-E184ED4A747E";
	setAttr ".txf" -type "matrix" 0.69520726615502138 0 0 0 0 0.69520726615502138 0 0
		 0 0 0.69520726615502138 0 0 0 0 1;
createNode skinCluster -n "skinCluster13";
	rename -uid "DDA438E3-4067-9804-7619-21AEE0F73C22";
	setAttr -s 7 ".wl";
	setAttr ".wl[0].w[6]"  1;
	setAttr ".wl[1].w[5]"  1;
	setAttr ".wl[2].w[4]"  1;
	setAttr ".wl[3].w[3]"  1;
	setAttr ".wl[4].w[2]"  1;
	setAttr ".wl[5].w[1]"  1;
	setAttr ".wl[6].w[0]"  1;
	setAttr -s 7 ".pm";
	setAttr ".pm[0]" -type "matrix" 2.2204460492503131e-016 -0 1 -0 0.22569590128716774 0.97419780339629847 -5.0114557234508026e-017 0
		 -0.97419780339629847 0.22569590128716774 2.1631536637396442e-016 -0 4.8096906772089145 -6.3429783868167586 -1.6675544373762101 1;
	setAttr ".pm[1]" -type "matrix" 2.2204460492503131e-016 -0 1 -0 0.22569590128716774 0.97419780339629847 -5.0114557234508026e-017 0
		 -0.97419780339629847 0.22569590128716774 2.1631536637396442e-016 -0 5.2773549743955943 -6.3429783868167577 -1.6675544373762103 1;
	setAttr ".pm[2]" -type "matrix" 0.70710678118654735 -0 0.70710678118654757 -0 0.15959110228616596 0.97419780339629836 -0.15959110228616591 0
		 -0.68886187299856172 0.22569590128716771 0.6888618729985615 -0 3.7316534891236843 -6.3429783868167569 -5.4375353572658769 1;
	setAttr ".pm[3]" -type "matrix" 1 -0 0 -0 -0 0.97419780339629847 -0.22569590128716774 0
		 0 0.22569590128716774 0.97419780339629847 -0 -0 -6.3429783868167569 -6.9449094117718042 1;
	setAttr ".pm[4]" -type "matrix" -0.70710678118654757 -0 0.70710678118654768 -0 0.15959110228616599 0.97419780339629869 0.15959110228616596 0
		 -0.68886187299856183 0.22569590128716779 -0.68886187299856172 0 3.7316534891236861 -6.3429783868167604 5.4375353572658787 1;
	setAttr ".pm[5]" -type "matrix" 2.2204460492503121e-016 -0 0.99999999999999978 -0
		 0.22569590128716768 0.97419780339629847 -5.0114557234508001e-017 0 -0.97419780339629825 0.22569590128716774 2.1631536637396432e-016 -0
		 5.2773549743955934 -6.3429783868167577 1.6675544373762077 1;
	setAttr ".pm[6]" -type "matrix" 2.2204460492503121e-016 -0 0.99999999999999978 -0
		 0.22569590128716768 0.97419780339629847 -5.0114557234508001e-017 0 -0.97419780339629825 0.22569590128716774 2.1631536637396432e-016 -0
		 4.8096906772089145 -6.3429783868167586 1.6675544373762079 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 7 ".ma";
	setAttr -s 7 ".dpf[0:6]"  4 4 4 4 4 4 4;
	setAttr -s 7 ".lw";
	setAttr -s 7 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 7 ".ifcl";
	setAttr -s 7 ".ifcl";
createNode tweak -n "tweak3";
	rename -uid "10A7D55C-4871-E488-769B-B583173E057A";
createNode objectSet -n "skinCluster13Set";
	rename -uid "8C975CC0-4F25-7879-0F72-3CAB729E6D4B";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster13GroupId";
	rename -uid "4C886128-4A19-CEEB-B055-82ACE1E04924";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster13GroupParts";
	rename -uid "20FBA888-42AE-0F0E-D396-28BEC0E80772";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode objectSet -n "tweakSet3";
	rename -uid "36CED2FC-44D0-D3C0-5BE3-1DAE67A60ADD";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId6";
	rename -uid "DBC76F6C-4C64-194E-23BF-03A8704EC9D4";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts6";
	rename -uid "BCFC2BD4-4BE7-48F2-BAEC-13876736EA77";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode dagPose -n "bindPose3";
	rename -uid "0D64554E-4C8F-FE7F-36EE-18A8D035D8C7";
	setAttr -s 14 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[6]" -type "matrix" 1 0 0 0 0 0.97419780339629847 0.22569590128716774 0
		 0 -0.22569590128716774 0.97419780339629847 0 0 4.9882382240685486 6.5727718476563508 1;
	setAttr -s 14 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 6.7213108154266488 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -1.0764664923223961
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -5.6448443231042527
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0.2276573097791999 0 0 0 0 4.9882382240685486
		 6.5727718476563508 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 1.5707963267948966 0 0 1.6675544373762092
		 1.7763568394002367e-015 -0.46766429718667984 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 1.5707963267948966 0 0 1.6675544373762092
		 1.7763568394002365e-015 -2.9586234853691068e-016 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.2062406368665213 1.7763568394002363e-015
		 1.2062406368665219 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.38268343236508984 0 0.92387953251128674 1
		 1 1 yes;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 1.7763568394002365e-015
		 1.6675544373762092 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 9.3224239734349157e-017 1.5707963267948966
		 0 0 -1.2062406368665213 1.7763568394002505e-015 1.2062406368665224 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.38268343236508984 0 0.92387953251128674 1 1 1 yes;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 -5.887846720064156e-017 1.5707963267948963
		 0 0 -1.6675544373762092 1.7763568394002505e-015 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 -5.887846720064156e-017 1.5707963267948963
		 0 0 -1.6675544373762092 2.6645352591003757e-015 -0.46766429718667979 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 14 ".m";
	setAttr -s 14 ".p";
	setAttr -s 14 ".g[0:13]" yes yes yes yes yes yes yes no no no no no 
		no no;
	setAttr ".bp" yes;
createNode skinCluster -n "skinCluster14";
	rename -uid "8C68765A-40C2-A8D6-6032-FA894AB9AD9A";
	setAttr -s 7 ".wl";
	setAttr ".wl[0].w[6]"  1;
	setAttr ".wl[1].w[5]"  1;
	setAttr ".wl[2].w[4]"  1;
	setAttr ".wl[3].w[3]"  1;
	setAttr ".wl[4].w[2]"  1;
	setAttr ".wl[5].w[1]"  1;
	setAttr ".wl[6].w[0]"  1;
	setAttr -s 7 ".pm";
	setAttr ".pm[0]" -type "matrix" 2.2204460492503131e-016 -0 1 -0 0.2453231345667933 0.96944136472832809 -5.4472678493853911e-017 0
		 -0.96944136472832809 0.2453231345667933 2.1525922482908479e-016 -0 4.6806177446671402 -5.258133983039083 -1.6675544373762103 1;
	setAttr ".pm[1]" -type "matrix" 0.33797885553820933 -1.387778780781446e-017 0.94115370328606907 -0
		 0.23088677659928422 0.9694413647283282 -0.082914032257930925 0 -0.91239333053276683 0.24532313456679336 0.32765068296228012 -0
		 4.7480327236071886 -5.2581339830390821 -3.4768912792178672 1;
	setAttr ".pm[2]" -type "matrix" 0.80180677205870898 -1.387778780781446e-017 0.59758338353805796 -0
		 0.14660102881458664 0.96944136472832809 -0.19670175063832482 0 -0.57932205087610678 0.24532313456679328 0.7773046513530103 -0
		 3.0420563115742238 -5.2581339830390812 -5.8465825780210778 1;
	setAttr ".pm[3]" -type "matrix" 1 -0 0 -0 -0 0.96944136472832809 -0.2453231345667933 0
		 0 0.2453231345667933 0.96944136472832809 -0 -0 -5.2581339830390812 -6.8379846395431212 1;
	setAttr ".pm[4]" -type "matrix" -0.80180677205870921 1.3877787807814466e-017 0.59758338353805807 -0
		 0.14660102881458667 0.96944136472832809 0.19670175063832487 0 -0.57932205087610678 0.24532313456679333 -0.77730465135301052 0
		 3.0420563115742247 -5.258133983039083 5.8465825780210796 1;
	setAttr ".pm[5]" -type "matrix" -0.33797885553820894 -0 0.9411537032860694 -0 0.2308867765992843 0.9694413647283282 0.082914032257930828 0
		 -0.91239333053276717 0.24532313456679339 -0.32765068296227973 0 4.7480327236071913 -5.2581339830390847 3.4768912792178654 1;
	setAttr ".pm[6]" -type "matrix" 4.4408920985006262e-016 -0 1 -0 0.2453231345667933 0.96944136472832809 -1.0894535698770782e-016 0
		 -0.96944136472832809 0.2453231345667933 4.3051844965816959e-016 -0 4.6806177446671402 -5.2581339830390847 1.6675544373762072 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 7 ".ma";
	setAttr -s 7 ".dpf[0:6]"  4 4 4 4 4 4 4;
	setAttr -s 7 ".lw";
	setAttr -s 7 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 7 ".ifcl";
	setAttr -s 7 ".ifcl";
createNode tweak -n "tweak4";
	rename -uid "611C8019-49CC-94B7-DDF1-3DBFF73EBCFD";
createNode objectSet -n "skinCluster14Set";
	rename -uid "E3E68139-4561-C63F-B52D-A1ADBA329D40";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster14GroupId";
	rename -uid "663C8191-4EA7-3582-6178-058B1E9C4B91";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster14GroupParts";
	rename -uid "015D480D-45F0-27A2-A937-CC84B6FD9B25";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode objectSet -n "tweakSet4";
	rename -uid "C81DF281-416B-7A40-F9C7-DEA15E03E654";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId8";
	rename -uid "1CC0918E-4985-BB41-FC5C-C0A7AD7BF473";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts8";
	rename -uid "310134AE-4470-F3D1-83B2-488FC207EAD1";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode dagPose -n "bindPose4";
	rename -uid "C85FB11D-4DC4-4012-C533-AFAE4E274E63";
	setAttr -s 14 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 6.7213108154266488 0 1;
	setAttr ".wm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 5.6448443231042527 0 1;
	setAttr ".wm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[6]" -type "matrix" 1 0 0 0 0 0.96944136472832787 0.24532313456679325 0
		 0 -0.24532313456679325 0.96944136472832787 0 0 3.8290264401873988 6.3023708221125805 1;
	setAttr ".wm[7]" -type "matrix" 2.2204460492503131e-016 0.24532313456679325 -0.96944136472832787 0
		 0 0.96944136472832787 0.24532313456679325 0 1 -5.4472678493853899e-017 2.1525922482908474e-016 0
		 1.6675544373762095 3.9491887676111106 5.8275263648530657 1;
	setAttr ".wm[8]" -type "matrix" 0.33797885553820939 0.23088677659928417 -0.91239333053276661 0
		 0 0.96944136472832787 0.24532313456679325 0 0.94115370328606918 -0.082914032257930911 0.32765068296228006 0
		 1.6675544373762095 3.7129115380178335 6.7612211030831801 1;
	setAttr ".wm[9]" -type "matrix" 0.80180677205870887 0.14660102881458661 -0.57932205087610666 0
		 0 0.96944136472832787 0.24532313456679325 0 0.59758338353805796 -0.19670175063832476 0.77730465135301008 0
		 1.0546792475043469 3.501450971104842 7.5968480444083664 1;
	setAttr ".wm[10]" -type "matrix" 1 0 0 0 0 0.96944136472832787 0.24532313456679325 0
		 0 -0.24532313456679325 0.96944136472832787 0 0 3.4199367585495035 7.9189670716413518 1;
	setAttr ".wm[11]" -type "matrix" -0.80180677205870876 0.14660102881458656 -0.57932205087610644 0
		 0 0.96944136472832787 0.24532313456679325 0 0.59758338353805773 0.19670175063832473 -0.77730465135300997 0
		 -1.0546792475043469 3.5014509711048429 7.5968480444083664 1;
	setAttr ".wm[12]" -type "matrix" -0.33797885553820883 0.23088677659928419 -0.91239333053276672 0
		 0 0.96944136472832787 0.24532313456679325 0 0.94115370328606929 0.082914032257930786 -0.32765068296227956 0
		 -1.6675544373762095 3.7129115380178344 6.761221103083181 1;
	setAttr ".wm[13]" -type "matrix" 4.4408920985006262e-016 0.24532313456679325 -0.96944136472832787 0
		 0 0.96944136472832787 0.24532313456679325 0 1 -1.089453569877078e-016 4.3051844965816949e-016 0
		 -1.6675544373762095 3.9491887676111115 5.8275263648530657 1;
	setAttr -s 14 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 6.7213108154266488 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -1.0764664923223961
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -5.6448443231042527
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 0.99999999999999989 0.99999999999999989 0.2478529988663877
		 0 0 0 0 3.8290264401873988 6.3023708221125805 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
		0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 1.5707963267948966 0 0 1.6675544373762095
		 3.5527136788004816e-015 -0.48981245749977242 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 1.2260277775807136 0 0 1.6675544373762095
		 1.7763568394002365e-015 0.47331411436026927 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 -0.14491441558751839 0 0 1.0546792475043469
		 1.7763568394002363e-015 1.335281605874683 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0.38268343236508984 0 0.92387953251128674 1 1 1 yes;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 1.7763568394002365e-015
		 1.6675544373762092 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 -8.8817841970012523e-016 1.7157107423824149
		 -8.8817841970012523e-016 0 -1.0546792475043469 2.6645352591003757e-015 1.3352816058746821 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.38268343236508984 0 0.92387953251128674 1
		 1 1 yes;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-016 1.9155648760090789
		 4.4408920985006262e-016 0 -1.6675544373762095 2.6645352591003757e-015 0.47331411436026993 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 7.8504622934188783e-017 1.5707963267948961
		 0 0 -1.6675544373762095 4.4408920985006262e-015 -0.48981245749977287 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 14 ".m";
	setAttr -s 14 ".p";
	setAttr -s 14 ".g[0:13]" yes yes yes yes yes yes yes no no no no no 
		no no;
	setAttr ".bp" yes;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr -av -k on ".unw" 1;
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -k on ".ihi";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av ".ta";
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -av ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".dsm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -k off -cb on ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off -cb on ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :ikSystem;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".gsn";
	setAttr -k on ".gsv";
	setAttr -s 4 ".sol";
connectAttr "L_Eye_00_Gross_Skeleton.s" "L_EyeBall_00_Skeleton.is";
connectAttr "R_Eye_00_Gross_Skeleton.s" "R_EyeBall_00_Skeleton.is";
connectAttr "M_JawUpper_Position_Skeleton.s" "M_JawUpperEnd_Skeleton.is";
connectAttr "M_JawLower_Position_Skeleton.s" "M_JawLowerEnd_Skeleton.is";
connectAttr "M_Tongue_00_Skeleton.s" "M_Tongue_01_Skeleton.is";
connectAttr "M_Tongue_01_Skeleton.s" "M_Tongue_02_Skeleton.is";
connectAttr "M_Tongue_02_Skeleton.s" "M_Tongue_03_Skeleton.is";
connectAttr "M_Tongue_03_Skeleton.s" "M_Tongue_04_Skeleton.is";
connectAttr "TeethUpper_Second_GRP_parentConstraint1.ctx" "TeethUpper_Second_GRP.tx"
		;
connectAttr "TeethUpper_Second_GRP_parentConstraint1.cty" "TeethUpper_Second_GRP.ty"
		;
connectAttr "TeethUpper_Second_GRP_parentConstraint1.ctz" "TeethUpper_Second_GRP.tz"
		;
connectAttr "TeethUpper_Second_GRP_parentConstraint1.crx" "TeethUpper_Second_GRP.rx"
		;
connectAttr "TeethUpper_Second_GRP_parentConstraint1.cry" "TeethUpper_Second_GRP.ry"
		;
connectAttr "TeethUpper_Second_GRP_parentConstraint1.crz" "TeethUpper_Second_GRP.rz"
		;
connectAttr "TeethUpper_Second_GRP_scaleConstraint1.csx" "TeethUpper_Second_GRP.sx"
		;
connectAttr "TeethUpper_Second_GRP_scaleConstraint1.csy" "TeethUpper_Second_GRP.sy"
		;
connectAttr "TeethUpper_Second_GRP_scaleConstraint1.csz" "TeethUpper_Second_GRP.sz"
		;
connectAttr "TeethUpper_Second_GRP.ro" "TeethUpper_Second_GRP_parentConstraint1.cro"
		;
connectAttr "TeethUpper_Second_GRP.pim" "TeethUpper_Second_GRP_parentConstraint1.cpim"
		;
connectAttr "TeethUpper_Second_GRP.rp" "TeethUpper_Second_GRP_parentConstraint1.crp"
		;
connectAttr "TeethUpper_Second_GRP.rpt" "TeethUpper_Second_GRP_parentConstraint1.crt"
		;
connectAttr "M_TeethUpper_00_Skeleton.t" "TeethUpper_Second_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_TeethUpper_00_Skeleton.rp" "TeethUpper_Second_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_TeethUpper_00_Skeleton.rpt" "TeethUpper_Second_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_TeethUpper_00_Skeleton.r" "TeethUpper_Second_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_TeethUpper_00_Skeleton.ro" "TeethUpper_Second_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_TeethUpper_00_Skeleton.s" "TeethUpper_Second_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_TeethUpper_00_Skeleton.pm" "TeethUpper_Second_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_TeethUpper_00_Skeleton.jo" "TeethUpper_Second_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_TeethUpper_00_Skeleton.ssc" "TeethUpper_Second_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_TeethUpper_00_Skeleton.is" "TeethUpper_Second_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "TeethUpper_Second_GRP_parentConstraint1.w0" "TeethUpper_Second_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "TeethUpper_Second_GRP.pim" "TeethUpper_Second_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_TeethUpper_00_Skeleton.s" "TeethUpper_Second_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_TeethUpper_00_Skeleton.pm" "TeethUpper_Second_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "TeethUpper_Second_GRP_scaleConstraint1.w0" "TeethUpper_Second_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "TeethLower_Second_GRP_parentConstraint1.ctx" "TeethLower_Second_GRP.tx"
		;
connectAttr "TeethLower_Second_GRP_parentConstraint1.cty" "TeethLower_Second_GRP.ty"
		;
connectAttr "TeethLower_Second_GRP_parentConstraint1.ctz" "TeethLower_Second_GRP.tz"
		;
connectAttr "TeethLower_Second_GRP_parentConstraint1.crx" "TeethLower_Second_GRP.rx"
		;
connectAttr "TeethLower_Second_GRP_parentConstraint1.cry" "TeethLower_Second_GRP.ry"
		;
connectAttr "TeethLower_Second_GRP_parentConstraint1.crz" "TeethLower_Second_GRP.rz"
		;
connectAttr "TeethLower_Second_GRP_scaleConstraint1.csx" "TeethLower_Second_GRP.sx"
		;
connectAttr "TeethLower_Second_GRP_scaleConstraint1.csy" "TeethLower_Second_GRP.sy"
		;
connectAttr "TeethLower_Second_GRP_scaleConstraint1.csz" "TeethLower_Second_GRP.sz"
		;
connectAttr "TeethLower_Second_GRP.ro" "TeethLower_Second_GRP_parentConstraint1.cro"
		;
connectAttr "TeethLower_Second_GRP.pim" "TeethLower_Second_GRP_parentConstraint1.cpim"
		;
connectAttr "TeethLower_Second_GRP.rp" "TeethLower_Second_GRP_parentConstraint1.crp"
		;
connectAttr "TeethLower_Second_GRP.rpt" "TeethLower_Second_GRP_parentConstraint1.crt"
		;
connectAttr "M_TeethLower_00_Skeleton.t" "TeethLower_Second_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_TeethLower_00_Skeleton.rp" "TeethLower_Second_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_TeethLower_00_Skeleton.rpt" "TeethLower_Second_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_TeethLower_00_Skeleton.r" "TeethLower_Second_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_TeethLower_00_Skeleton.ro" "TeethLower_Second_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_TeethLower_00_Skeleton.s" "TeethLower_Second_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_TeethLower_00_Skeleton.pm" "TeethLower_Second_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_TeethLower_00_Skeleton.jo" "TeethLower_Second_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_TeethLower_00_Skeleton.ssc" "TeethLower_Second_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_TeethLower_00_Skeleton.is" "TeethLower_Second_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "TeethLower_Second_GRP_parentConstraint1.w0" "TeethLower_Second_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "TeethLower_Second_GRP.pim" "TeethLower_Second_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_TeethLower_00_Skeleton.s" "TeethLower_Second_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_TeethLower_00_Skeleton.pm" "TeethLower_Second_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "TeethLower_Second_GRP_scaleConstraint1.w0" "TeethLower_Second_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_NoseUpper_Skeleton.s" "M_Nose_00_Skeleton.is";
connectAttr "M_Nose_00_Skeleton.s" "M_NoseTip_00_Skeleton.is";
connectAttr "M_Nose_00_Skeleton.s" "M_NoseUnder_00_Skeleton.is";
connectAttr "M_Nose_00_Skeleton.s" "L_NoseConner_00_Skeleton.is";
connectAttr "M_Nose_00_Skeleton.s" "R_NoseConner_00_Skeleton.is";
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_Check_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_Check_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_Check_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_Check_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_Check_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_Check_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_Check_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_Check_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_Check_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP.ro" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP.pim" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP.rp" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP.rpt" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_Cheek_00_Skeleton.t" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_Cheek_00_Skeleton.rp" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_Cheek_00_Skeleton.rpt" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_Cheek_00_Skeleton.r" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_Cheek_00_Skeleton.ro" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_Cheek_00_Skeleton.s" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_Cheek_00_Skeleton.pm" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_Cheek_00_Skeleton.jo" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_Cheek_00_Skeleton.ssc" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_Cheek_00_Skeleton.is" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP.pim" "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_Cheek_00_Skeleton.s" "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_Cheek_00_Skeleton.pm" "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_Check_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_Check_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_Check_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_Check_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_Check_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_Check_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_Check_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_Check_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_Check_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP.ro" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP.pim" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP.rp" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP.rpt" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_Cheek_00_Skeleton.t" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_Cheek_00_Skeleton.rp" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_Cheek_00_Skeleton.rpt" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_Cheek_00_Skeleton.r" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_Cheek_00_Skeleton.ro" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_Cheek_00_Skeleton.s" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_Cheek_00_Skeleton.pm" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_Cheek_00_Skeleton.jo" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_Cheek_00_Skeleton.ssc" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_Cheek_00_Skeleton.is" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_Check_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP.pim" "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_Cheek_00_Skeleton.s" "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_Cheek_00_Skeleton.pm" "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_Check_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidOuter_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_LidOuter_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidOuter_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_LidOuter_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_LidOuter_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_LidOuter_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidOuter_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidOuter_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidOuter_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP.ro" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP.pim" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP.rp" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP.rpt" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidUpper_02_Skeleton.t" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidUpper_02_Skeleton.rp" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidUpper_02_Skeleton.rpt" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidUpper_02_Skeleton.r" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidUpper_02_Skeleton.ro" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidUpper_02_Skeleton.s" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_02_Skeleton.pm" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_02_Skeleton.jo" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidUpper_02_Skeleton.ssc" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidUpper_02_Skeleton.is" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP.pim" "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidUpper_02_Skeleton.s" "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_02_Skeleton.pm" "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidInner_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_LidInner_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidInner_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_LidInner_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_LidInner_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_LidInner_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidInner_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidInner_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidInner_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP.ro" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP.pim" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP.rp" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP.rpt" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidInner_00_Skeleton.t" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidInner_00_Skeleton.rp" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidInner_00_Skeleton.rpt" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidInner_00_Skeleton.r" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidInner_00_Skeleton.ro" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidInner_00_Skeleton.s" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidInner_00_Skeleton.pm" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidInner_00_Skeleton.jo" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidInner_00_Skeleton.ssc" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidInner_00_Skeleton.is" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP.pim" "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidInner_00_Skeleton.s" "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidInner_00_Skeleton.pm" "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketLower_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketLower_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketLower_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketLower_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketLower_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketLower_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketLower_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketLower_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketLower_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP.ro" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP.pim" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP.rp" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP.rpt" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketLower_01_Skeleton.t" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketLower_01_Skeleton.rp" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketLower_01_Skeleton.rpt" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketLower_01_Skeleton.r" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketLower_01_Skeleton.ro" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketLower_01_Skeleton.s" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketLower_01_Skeleton.pm" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketLower_01_Skeleton.jo" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketLower_01_Skeleton.ssc" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketLower_01_Skeleton.is" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP.pim" "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketLower_01_Skeleton.s" "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketLower_01_Skeleton.pm" "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketUpper_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketUpper_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketUpper_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketUpper_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketUpper_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketUpper_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketUpper_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketUpper_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketUpper_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP.ro" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP.pim" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP.rp" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP.rpt" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketUpper_01_Skeleton.t" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketUpper_01_Skeleton.rp" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketUpper_01_Skeleton.rpt" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketUpper_01_Skeleton.r" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketUpper_01_Skeleton.ro" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketUpper_01_Skeleton.s" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketUpper_01_Skeleton.pm" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketUpper_01_Skeleton.jo" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketUpper_01_Skeleton.ssc" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketUpper_01_Skeleton.is" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP.pim" "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketUpper_01_Skeleton.s" "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketUpper_01_Skeleton.pm" "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketLower_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketLower_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketLower_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketLower_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketLower_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketLower_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketLower_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketLower_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketLower_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP.ro" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP.pim" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP.rp" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP.rpt" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketLower_01_Skeleton.t" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketLower_01_Skeleton.rp" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketLower_01_Skeleton.rpt" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketLower_01_Skeleton.r" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketLower_01_Skeleton.ro" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketLower_01_Skeleton.s" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketLower_01_Skeleton.pm" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketLower_01_Skeleton.jo" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketLower_01_Skeleton.ssc" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketLower_01_Skeleton.is" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP.pim" "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketLower_01_Skeleton.s" "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketLower_01_Skeleton.pm" "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketUpper_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketUpper_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketUpper_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketUpper_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketUpper_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketUpper_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketUpper_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketUpper_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketUpper_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP.ro" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP.pim" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP.rp" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP.rpt" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketUpper_01_Skeleton.t" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketUpper_01_Skeleton.rp" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketUpper_01_Skeleton.rpt" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketUpper_01_Skeleton.r" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketUpper_01_Skeleton.ro" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketUpper_01_Skeleton.s" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketUpper_01_Skeleton.pm" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketUpper_01_Skeleton.jo" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketUpper_01_Skeleton.ssc" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketUpper_01_Skeleton.is" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP.pim" "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketUpper_01_Skeleton.s" "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketUpper_01_Skeleton.pm" "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidLower_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_LidLower_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidLower_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_LidLower_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_LidLower_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_LidLower_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidLower_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidLower_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidLower_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP.ro" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP.pim" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP.rp" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP.rpt" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidLower_01_Skeleton.t" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidLower_01_Skeleton.rp" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidLower_01_Skeleton.rpt" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidLower_01_Skeleton.r" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidLower_01_Skeleton.ro" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidLower_01_Skeleton.s" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidLower_01_Skeleton.pm" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidLower_01_Skeleton.jo" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidLower_01_Skeleton.ssc" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidLower_01_Skeleton.is" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP.pim" "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidLower_01_Skeleton.s" "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidLower_01_Skeleton.pm" "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidUpper_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_LidUpper_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidUpper_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_LidUpper_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_LidUpper_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_LidUpper_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidUpper_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidUpper_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidUpper_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP.ro" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP.pim" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP.rp" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP.rpt" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidUpper_01_Skeleton.t" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidUpper_01_Skeleton.rp" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidUpper_01_Skeleton.rpt" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidUpper_01_Skeleton.r" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidUpper_01_Skeleton.ro" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidUpper_01_Skeleton.s" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_01_Skeleton.pm" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_01_Skeleton.jo" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidUpper_01_Skeleton.ssc" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidUpper_01_Skeleton.is" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP.pim" "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidUpper_01_Skeleton.s" "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_01_Skeleton.pm" "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidLower_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_LidLower_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidLower_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_LidLower_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_LidLower_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_LidLower_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidLower_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidLower_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidLower_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP.ro" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP.pim" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP.rp" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP.rpt" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidLower_01_Skeleton.t" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidLower_01_Skeleton.rp" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidLower_01_Skeleton.rpt" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidLower_01_Skeleton.r" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidLower_01_Skeleton.ro" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidLower_01_Skeleton.s" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidLower_01_Skeleton.pm" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidLower_01_Skeleton.jo" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidLower_01_Skeleton.ssc" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidLower_01_Skeleton.is" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_LidLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP.pim" "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidLower_01_Skeleton.s" "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidLower_01_Skeleton.pm" "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidUpper_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_LidUpper_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidUpper_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_LidUpper_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_LidUpper_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_LidUpper_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidUpper_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidUpper_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidUpper_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP.ro" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP.pim" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP.rp" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP.rpt" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidUpper_01_Skeleton.t" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidUpper_01_Skeleton.rp" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidUpper_01_Skeleton.rpt" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidUpper_01_Skeleton.r" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidUpper_01_Skeleton.ro" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidUpper_01_Skeleton.s" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidUpper_01_Skeleton.pm" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidUpper_01_Skeleton.jo" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidUpper_01_Skeleton.ssc" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidUpper_01_Skeleton.is" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_LidUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP.pim" "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidUpper_01_Skeleton.s" "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidUpper_01_Skeleton.pm" "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidInner_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_LidInner_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidInner_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_LidInner_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_LidInner_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_LidInner_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidInner_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidInner_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidInner_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP.ro" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP.pim" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP.rp" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP.rpt" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidInner_00_Skeleton.t" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidInner_00_Skeleton.rp" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidInner_00_Skeleton.rpt" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidInner_00_Skeleton.r" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidInner_00_Skeleton.ro" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidInner_00_Skeleton.s" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidInner_00_Skeleton.pm" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidInner_00_Skeleton.jo" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidInner_00_Skeleton.ssc" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidInner_00_Skeleton.is" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_LidInner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP.pim" "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidInner_00_Skeleton.s" "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidInner_00_Skeleton.pm" "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidInner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidOuter_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_LidOuter_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidOuter_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_LidOuter_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_LidOuter_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_LidOuter_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidOuter_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidOuter_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidOuter_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP.ro" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP.pim" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP.rp" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP.rpt" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidOuter_00_Skeleton.t" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidOuter_00_Skeleton.rp" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidOuter_00_Skeleton.rpt" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidOuter_00_Skeleton.r" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidOuter_00_Skeleton.ro" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidOuter_00_Skeleton.s" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidOuter_00_Skeleton.pm" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidOuter_00_Skeleton.jo" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidOuter_00_Skeleton.ssc" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidOuter_00_Skeleton.is" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_LidOuter_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP.pim" "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidOuter_00_Skeleton.s" "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidOuter_00_Skeleton.pm" "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidOuter_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "M_Nose_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "M_Nose_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "M_Nose_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "M_Nose_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "M_Nose_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "M_Nose_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "M_Nose_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "M_Nose_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "M_Nose_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP.ro" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP.pim" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP.rp" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP.rpt" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "M_Nose_00_Skeleton.t" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_Nose_00_Skeleton.rp" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_Nose_00_Skeleton.rpt" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_Nose_00_Skeleton.r" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_Nose_00_Skeleton.ro" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_Nose_00_Skeleton.s" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_Nose_00_Skeleton.pm" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_Nose_00_Skeleton.jo" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_Nose_00_Skeleton.ssc" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_Nose_00_Skeleton.is" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "M_Nose_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP.pim" "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_Nose_00_Skeleton.s" "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_Nose_00_Skeleton.pm" "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "M_Nose_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "M_NoseUpper_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "M_NoseUpper_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "M_NoseUpper_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "M_NoseUpper_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "M_NoseUpper_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "M_NoseUpper_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "M_NoseUpper_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "M_NoseUpper_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "M_NoseUpper_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP.ro" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP.pim" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP.rp" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP.rpt" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "M_NoseUpper_Skeleton.t" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_NoseUpper_Skeleton.rp" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_NoseUpper_Skeleton.rpt" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_NoseUpper_Skeleton.r" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_NoseUpper_Skeleton.ro" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_NoseUpper_Skeleton.s" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_NoseUpper_Skeleton.pm" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_NoseUpper_Skeleton.jo" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_NoseUpper_Skeleton.ssc" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_NoseUpper_Skeleton.is" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "M_NoseUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP.pim" "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_NoseUpper_Skeleton.s" "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_NoseUpper_Skeleton.pm" "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "M_NoseUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "M_Mouth_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "M_Mouth_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "M_Mouth_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "M_Mouth_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "M_Mouth_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "M_Mouth_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "M_Mouth_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "M_Mouth_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "M_Mouth_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP.ro" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP.pim" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP.rp" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP.rpt" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "M_LipUpper_00_Skeleton.t" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_LipUpper_00_Skeleton.rp" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_LipUpper_00_Skeleton.rpt" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_LipUpper_00_Skeleton.r" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_LipUpper_00_Skeleton.ro" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_LipUpper_00_Skeleton.s" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_LipUpper_00_Skeleton.pm" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_LipUpper_00_Skeleton.jo" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_LipUpper_00_Skeleton.ssc" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_LipUpper_00_Skeleton.is" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "M_LipLower_00_Skeleton.t" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].tt"
		;
connectAttr "M_LipLower_00_Skeleton.rp" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].trp"
		;
connectAttr "M_LipLower_00_Skeleton.rpt" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].trt"
		;
connectAttr "M_LipLower_00_Skeleton.r" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].tr"
		;
connectAttr "M_LipLower_00_Skeleton.ro" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].tro"
		;
connectAttr "M_LipLower_00_Skeleton.s" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].ts"
		;
connectAttr "M_LipLower_00_Skeleton.pm" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].tpm"
		;
connectAttr "M_LipLower_00_Skeleton.jo" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].tjo"
		;
connectAttr "M_LipLower_00_Skeleton.ssc" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].tsc"
		;
connectAttr "M_LipLower_00_Skeleton.is" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].tis"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.w1" "M_Mouth_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[1].tw"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP.pim" "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_LipUpper_00_Skeleton.s" "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_LipUpper_00_Skeleton.pm" "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_LipLower_00_Skeleton.s" "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[1].ts"
		;
connectAttr "M_LipLower_00_Skeleton.pm" "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[1].tpm"
		;
connectAttr "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.w1" "M_Mouth_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[1].tw"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_LipConner_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_LipConner_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_LipConner_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_LipConner_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_LipConner_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_LipConner_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_LipConner_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_LipConner_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_LipConner_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP.ro" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP.pim" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP.rp" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP.rpt" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LipConner_00_Skeleton.t" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LipConner_00_Skeleton.rp" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LipConner_00_Skeleton.rpt" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LipConner_00_Skeleton.r" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LipConner_00_Skeleton.ro" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LipConner_00_Skeleton.s" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LipConner_00_Skeleton.pm" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LipConner_00_Skeleton.jo" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LipConner_00_Skeleton.ssc" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LipConner_00_Skeleton.is" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP.pim" "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LipConner_00_Skeleton.s" "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LipConner_00_Skeleton.pm" "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_LipConner_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_LipConner_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_LipConner_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_LipConner_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_LipConner_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_LipConner_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_LipConner_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_LipConner_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_LipConner_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP.ro" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP.pim" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP.rp" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP.rpt" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LipConner_00_Skeleton.t" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LipConner_00_Skeleton.rp" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LipConner_00_Skeleton.rpt" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LipConner_00_Skeleton.r" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LipConner_00_Skeleton.ro" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LipConner_00_Skeleton.s" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LipConner_00_Skeleton.pm" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LipConner_00_Skeleton.jo" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LipConner_00_Skeleton.ssc" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LipConner_00_Skeleton.is" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_LipConner_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP.pim" "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LipConner_00_Skeleton.s" "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LipConner_00_Skeleton.pm" "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_LipConner_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "M_LipLower_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "M_LipLower_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "M_LipLower_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "M_LipLower_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "M_LipLower_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "M_LipLower_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "M_LipLower_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "M_LipLower_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "M_LipLower_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP.ro" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP.pim" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP.rp" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP.rpt" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "M_LipLower_00_Skeleton.t" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_LipLower_00_Skeleton.rp" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_LipLower_00_Skeleton.rpt" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_LipLower_00_Skeleton.r" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_LipLower_00_Skeleton.ro" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_LipLower_00_Skeleton.s" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_LipLower_00_Skeleton.pm" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_LipLower_00_Skeleton.jo" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_LipLower_00_Skeleton.ssc" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_LipLower_00_Skeleton.is" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "M_LipLower_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP.pim" "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_LipLower_00_Skeleton.s" "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_LipLower_00_Skeleton.pm" "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "M_LipLower_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "M_LipUpper_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "M_LipUpper_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "M_LipUpper_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "M_LipUpper_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "M_LipUpper_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "M_LipUpper_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "M_LipUpper_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "M_LipUpper_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "M_LipUpper_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP.ro" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP.pim" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP.rp" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP.rpt" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "M_LipUpper_00_Skeleton.t" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_LipUpper_00_Skeleton.rp" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_LipUpper_00_Skeleton.rpt" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_LipUpper_00_Skeleton.r" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_LipUpper_00_Skeleton.ro" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_LipUpper_00_Skeleton.s" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_LipUpper_00_Skeleton.pm" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_LipUpper_00_Skeleton.jo" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_LipUpper_00_Skeleton.ssc" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_LipUpper_00_Skeleton.is" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "M_LipUpper_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP.pim" "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_LipUpper_00_Skeleton.s" "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_LipUpper_00_Skeleton.pm" "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "M_LipUpper_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_BrowOuter_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_BrowOuter_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_BrowOuter_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_BrowOuter_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_BrowOuter_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_BrowOuter_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_BrowOuter_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_BrowOuter_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_BrowOuter_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP.ro" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP.pim" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP.rp" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP.rpt" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_Brow_03_Skeleton.t" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_Brow_03_Skeleton.rp" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_Brow_03_Skeleton.rpt" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_Brow_03_Skeleton.r" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_Brow_03_Skeleton.ro" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_Brow_03_Skeleton.s" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_Brow_03_Skeleton.pm" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_Brow_03_Skeleton.jo" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_Brow_03_Skeleton.ssc" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_Brow_03_Skeleton.is" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP.pim" "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_Brow_03_Skeleton.s" "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_Brow_03_Skeleton.pm" "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_BrowMiddle_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_BrowMiddle_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_BrowMiddle_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_BrowMiddle_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_BrowMiddle_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_BrowMiddle_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_BrowMiddle_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_BrowMiddle_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_BrowMiddle_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP.ro" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP.pim" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP.rp" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP.rpt" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_Brow_02_Skeleton.t" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_Brow_02_Skeleton.rp" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_Brow_02_Skeleton.rpt" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_Brow_02_Skeleton.r" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_Brow_02_Skeleton.ro" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_Brow_02_Skeleton.s" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_Brow_02_Skeleton.pm" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_Brow_02_Skeleton.jo" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_Brow_02_Skeleton.ssc" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_Brow_02_Skeleton.is" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP.pim" "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_Brow_02_Skeleton.s" "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_Brow_02_Skeleton.pm" "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_BrowInner_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_BrowInner_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_BrowInner_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_BrowInner_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_BrowInner_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_BrowInner_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_BrowInner_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_BrowInner_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_BrowInner_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP.ro" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP.pim" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP.rp" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP.rpt" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_Brow_00_Skeleton.t" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_Brow_00_Skeleton.rp" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_Brow_00_Skeleton.rpt" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_Brow_00_Skeleton.r" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_Brow_00_Skeleton.ro" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_Brow_00_Skeleton.s" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_Brow_00_Skeleton.pm" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_Brow_00_Skeleton.jo" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_Brow_00_Skeleton.ssc" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_Brow_00_Skeleton.is" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP.pim" "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_Brow_00_Skeleton.s" "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_Brow_00_Skeleton.pm" "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_BrowOuter_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_BrowOuter_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_BrowOuter_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_BrowOuter_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_BrowOuter_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_BrowOuter_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_BrowOuter_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_BrowOuter_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_BrowOuter_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP.ro" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP.pim" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP.rp" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP.rpt" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_Brow_03_Skeleton.t" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_Brow_03_Skeleton.rp" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_Brow_03_Skeleton.rpt" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_Brow_03_Skeleton.r" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_Brow_03_Skeleton.ro" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_Brow_03_Skeleton.s" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_Brow_03_Skeleton.pm" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_Brow_03_Skeleton.jo" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_Brow_03_Skeleton.ssc" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_Brow_03_Skeleton.is" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_BrowOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP.pim" "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_Brow_03_Skeleton.s" "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_Brow_03_Skeleton.pm" "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_BrowOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_BrowMiddle_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_BrowMiddle_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_BrowMiddle_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_BrowMiddle_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_BrowMiddle_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_BrowMiddle_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_BrowMiddle_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_BrowMiddle_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_BrowMiddle_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP.ro" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP.pim" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP.rp" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP.rpt" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_Brow_02_Skeleton.t" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_Brow_02_Skeleton.rp" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_Brow_02_Skeleton.rpt" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_Brow_02_Skeleton.r" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_Brow_02_Skeleton.ro" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_Brow_02_Skeleton.s" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_Brow_02_Skeleton.pm" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_Brow_02_Skeleton.jo" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_Brow_02_Skeleton.ssc" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_Brow_02_Skeleton.is" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_BrowMiddle_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP.pim" "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_Brow_02_Skeleton.s" "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_Brow_02_Skeleton.pm" "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_BrowMiddle_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_BrowInner_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_BrowInner_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_BrowInner_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_BrowInner_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_BrowInner_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_BrowInner_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_BrowInner_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_BrowInner_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_BrowInner_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP.ro" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP.pim" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP.rp" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP.rpt" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_Brow_00_Skeleton.t" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_Brow_00_Skeleton.rp" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_Brow_00_Skeleton.rpt" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_Brow_00_Skeleton.r" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_Brow_00_Skeleton.ro" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_Brow_00_Skeleton.s" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_Brow_00_Skeleton.pm" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_Brow_00_Skeleton.jo" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_Brow_00_Skeleton.ssc" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_Brow_00_Skeleton.is" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_BrowInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP.pim" "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_Brow_00_Skeleton.s" "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_Brow_00_Skeleton.pm" "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_BrowInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_Brow_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_Brow_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_Brow_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_Brow_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_Brow_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_Brow_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_Brow_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_Brow_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_Brow_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP.ro" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP.pim" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP.rp" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP.rpt" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_Brow_01_Skeleton.t" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_Brow_01_Skeleton.rp" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_Brow_01_Skeleton.rpt" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_Brow_01_Skeleton.r" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_Brow_01_Skeleton.ro" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_Brow_01_Skeleton.s" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_Brow_01_Skeleton.pm" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_Brow_01_Skeleton.jo" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_Brow_01_Skeleton.ssc" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_Brow_01_Skeleton.is" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP.pim" "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_Brow_01_Skeleton.s" "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_Brow_01_Skeleton.pm" "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_Brow_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_Brow_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_Brow_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_Brow_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_Brow_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_Brow_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_Brow_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_Brow_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_Brow_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP.ro" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP.pim" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP.rp" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP.rpt" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_Brow_01_Skeleton.t" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_Brow_01_Skeleton.rp" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_Brow_01_Skeleton.rpt" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_Brow_01_Skeleton.r" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_Brow_01_Skeleton.ro" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_Brow_01_Skeleton.s" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_Brow_01_Skeleton.pm" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_Brow_01_Skeleton.jo" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_Brow_01_Skeleton.ssc" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_Brow_01_Skeleton.is" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_Brow_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP.pim" "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_Brow_01_Skeleton.s" "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_Brow_01_Skeleton.pm" "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_Brow_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "R_Orbit_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "R_Orbit_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "R_Orbit_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "R_Orbit_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "R_Orbit_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "R_Orbit_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "R_Orbit_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "R_Orbit_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "R_Orbit_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP.ro" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP.pim" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP.rp" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP.rpt" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_Orbit_02_Skeleton.t" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_Orbit_02_Skeleton.rp" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_Orbit_02_Skeleton.rpt" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_Orbit_02_Skeleton.r" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_Orbit_02_Skeleton.ro" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_Orbit_02_Skeleton.s" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_Orbit_02_Skeleton.pm" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_Orbit_02_Skeleton.jo" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_Orbit_02_Skeleton.ssc" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_Orbit_02_Skeleton.is" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "R_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP.pim" "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_Orbit_02_Skeleton.s" "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_Orbit_02_Skeleton.pm" "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "R_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.ctx" "L_Orbit_00_Gross_CtrlPosition_GRP.tx"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.cty" "L_Orbit_00_Gross_CtrlPosition_GRP.ty"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.ctz" "L_Orbit_00_Gross_CtrlPosition_GRP.tz"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.crx" "L_Orbit_00_Gross_CtrlPosition_GRP.rx"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.cry" "L_Orbit_00_Gross_CtrlPosition_GRP.ry"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.crz" "L_Orbit_00_Gross_CtrlPosition_GRP.rz"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.csx" "L_Orbit_00_Gross_CtrlPosition_GRP.sx"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.csy" "L_Orbit_00_Gross_CtrlPosition_GRP.sy"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.csz" "L_Orbit_00_Gross_CtrlPosition_GRP.sz"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP.ro" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP.pim" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP.rp" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP.rpt" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_Orbit_02_Skeleton.t" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_Orbit_02_Skeleton.rp" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_Orbit_02_Skeleton.rpt" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_Orbit_02_Skeleton.r" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_Orbit_02_Skeleton.ro" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_Orbit_02_Skeleton.s" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_Orbit_02_Skeleton.pm" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_Orbit_02_Skeleton.jo" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_Orbit_02_Skeleton.ssc" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_Orbit_02_Skeleton.is" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.w0" "L_Orbit_00_Gross_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP.pim" "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_Orbit_02_Skeleton.s" "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_Orbit_02_Skeleton.pm" "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.w0" "L_Orbit_00_Gross_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "M_LipUpper_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "M_LipUpper_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "M_LipUpper_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "M_LipUpper_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "M_LipUpper_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "M_LipUpper_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "M_LipUpper_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "M_LipUpper_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "M_LipUpper_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP.ro" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP.pim" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP.rp" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP.rpt" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "M_LipUpper_00_Skeleton.t" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_LipUpper_00_Skeleton.rp" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_LipUpper_00_Skeleton.rpt" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_LipUpper_00_Skeleton.r" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_LipUpper_00_Skeleton.ro" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_LipUpper_00_Skeleton.s" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_LipUpper_00_Skeleton.pm" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_LipUpper_00_Skeleton.jo" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_LipUpper_00_Skeleton.ssc" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_LipUpper_00_Skeleton.is" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "M_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP.pim" "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_LipUpper_00_Skeleton.s" "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_LipUpper_00_Skeleton.pm" "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "M_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LipUpper_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LipUpper_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LipUpper_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LipUpper_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LipUpper_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LipUpper_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LipUpper_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LipUpper_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LipUpper_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP.ro" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP.pim" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP.rp" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP.rpt" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LipUpper_01_Skeleton.t" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LipUpper_01_Skeleton.rp" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LipUpper_01_Skeleton.rpt" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LipUpper_01_Skeleton.r" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LipUpper_01_Skeleton.ro" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LipUpper_01_Skeleton.s" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LipUpper_01_Skeleton.pm" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LipUpper_01_Skeleton.jo" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LipUpper_01_Skeleton.ssc" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LipUpper_01_Skeleton.is" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP.pim" "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LipUpper_01_Skeleton.s" "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LipUpper_01_Skeleton.pm" "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LipLower_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LipLower_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LipLower_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LipLower_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LipLower_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LipLower_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LipLower_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LipLower_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LipLower_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP.ro" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP.pim" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP.rp" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP.rpt" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LipLower_01_Skeleton.t" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LipLower_01_Skeleton.rp" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LipLower_01_Skeleton.rpt" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LipLower_01_Skeleton.r" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LipLower_01_Skeleton.ro" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LipLower_01_Skeleton.s" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LipLower_01_Skeleton.pm" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LipLower_01_Skeleton.jo" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LipLower_01_Skeleton.ssc" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LipLower_01_Skeleton.is" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP.pim" "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LipLower_01_Skeleton.s" "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LipLower_01_Skeleton.pm" "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "M_LipLower_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "M_LipLower_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "M_LipLower_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "M_LipLower_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "M_LipLower_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "M_LipLower_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "M_LipLower_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "M_LipLower_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "M_LipLower_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP.ro" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP.pim" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP.rp" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP.rpt" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "M_LipLower_00_Skeleton.t" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "M_LipLower_00_Skeleton.rp" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "M_LipLower_00_Skeleton.rpt" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "M_LipLower_00_Skeleton.r" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "M_LipLower_00_Skeleton.ro" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "M_LipLower_00_Skeleton.s" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "M_LipLower_00_Skeleton.pm" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "M_LipLower_00_Skeleton.jo" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "M_LipLower_00_Skeleton.ssc" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "M_LipLower_00_Skeleton.is" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "M_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP.pim" "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "M_LipLower_00_Skeleton.s" "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "M_LipLower_00_Skeleton.pm" "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "M_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LipUpper_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LipUpper_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LipUpper_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LipUpper_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LipUpper_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LipUpper_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LipUpper_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LipUpper_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LipUpper_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP.ro" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP.pim" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP.rp" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP.rpt" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LipUpper_01_Skeleton.t" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LipUpper_01_Skeleton.rp" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LipUpper_01_Skeleton.rpt" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LipUpper_01_Skeleton.r" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LipUpper_01_Skeleton.ro" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LipUpper_01_Skeleton.s" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LipUpper_01_Skeleton.pm" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LipUpper_01_Skeleton.jo" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LipUpper_01_Skeleton.ssc" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LipUpper_01_Skeleton.is" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LipUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP.pim" "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LipUpper_01_Skeleton.s" "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LipUpper_01_Skeleton.pm" "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LipUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LipLower_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LipLower_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LipLower_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LipLower_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LipLower_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LipLower_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LipLower_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LipLower_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LipLower_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP.ro" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP.pim" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP.rp" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP.rpt" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LipLower_01_Skeleton.t" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LipLower_01_Skeleton.rp" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LipLower_01_Skeleton.rpt" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LipLower_01_Skeleton.r" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LipLower_01_Skeleton.ro" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LipLower_01_Skeleton.s" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LipLower_01_Skeleton.pm" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LipLower_01_Skeleton.jo" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LipLower_01_Skeleton.ssc" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LipLower_01_Skeleton.is" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LipLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP.pim" "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LipLower_01_Skeleton.s" "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LipLower_01_Skeleton.pm" "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LipLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LipConner_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LipConner_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LipConner_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LipConner_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LipConner_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LipConner_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LipConner_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LipConner_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LipConner_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP.ro" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP.pim" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP.rp" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP.rpt" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LipConner_00_Skeleton.t" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LipConner_00_Skeleton.rp" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LipConner_00_Skeleton.rpt" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LipConner_00_Skeleton.r" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LipConner_00_Skeleton.ro" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LipConner_00_Skeleton.s" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LipConner_00_Skeleton.pm" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LipConner_00_Skeleton.jo" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LipConner_00_Skeleton.ssc" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LipConner_00_Skeleton.is" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP.pim" "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LipConner_00_Skeleton.s" "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LipConner_00_Skeleton.pm" "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LipConner_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LipConner_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LipConner_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LipConner_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LipConner_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LipConner_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LipConner_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LipConner_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LipConner_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP.ro" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP.pim" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP.rp" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP.rpt" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LipConner_00_Skeleton.t" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LipConner_00_Skeleton.rp" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LipConner_00_Skeleton.rpt" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LipConner_00_Skeleton.r" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LipConner_00_Skeleton.ro" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LipConner_00_Skeleton.s" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LipConner_00_Skeleton.pm" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LipConner_00_Skeleton.jo" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LipConner_00_Skeleton.ssc" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LipConner_00_Skeleton.is" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LipConner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP.pim" "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LipConner_00_Skeleton.s" "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LipConner_00_Skeleton.pm" "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LipConner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidUpper_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LidUpper_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidUpper_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LidUpper_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LidUpper_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LidUpper_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidUpper_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidUpper_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidUpper_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP.ro" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP.pim" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP.rp" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP.rpt" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidUpper_00_Skeleton.t" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidUpper_00_Skeleton.rp" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidUpper_00_Skeleton.rpt" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidUpper_00_Skeleton.r" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidUpper_00_Skeleton.ro" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidUpper_00_Skeleton.s" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidUpper_00_Skeleton.pm" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidUpper_00_Skeleton.jo" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidUpper_00_Skeleton.ssc" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidUpper_00_Skeleton.is" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP.pim" "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidUpper_00_Skeleton.s" "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidUpper_00_Skeleton.pm" "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidUpper_01_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LidUpper_01_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidUpper_01_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LidUpper_01_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LidUpper_01_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LidUpper_01_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidUpper_01_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidUpper_01_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidUpper_01_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP.ro" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP.pim" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP.rp" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP.rpt" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidUpper_01_Skeleton.t" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidUpper_01_Skeleton.rp" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidUpper_01_Skeleton.rpt" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidUpper_01_Skeleton.r" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidUpper_01_Skeleton.ro" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidUpper_01_Skeleton.s" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidUpper_01_Skeleton.pm" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidUpper_01_Skeleton.jo" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidUpper_01_Skeleton.ssc" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidUpper_01_Skeleton.is" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP.pim" "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidUpper_01_Skeleton.s" "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidUpper_01_Skeleton.pm" "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidUpper_02_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LidUpper_02_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidUpper_02_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LidUpper_02_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LidUpper_02_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LidUpper_02_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidUpper_02_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidUpper_02_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidUpper_02_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP.ro" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP.pim" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP.rp" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP.rpt" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidUpper_02_Skeleton.t" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidUpper_02_Skeleton.rp" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidUpper_02_Skeleton.rpt" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidUpper_02_Skeleton.r" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidUpper_02_Skeleton.ro" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidUpper_02_Skeleton.s" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidUpper_02_Skeleton.pm" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidUpper_02_Skeleton.jo" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidUpper_02_Skeleton.ssc" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidUpper_02_Skeleton.is" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP.pim" "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidUpper_02_Skeleton.s" "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidUpper_02_Skeleton.pm" "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidLower_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LidLower_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidLower_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LidLower_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LidLower_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LidLower_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidLower_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidLower_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidLower_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP.ro" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP.pim" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP.rp" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP.rpt" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidLower_00_Skeleton.t" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidLower_00_Skeleton.rp" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidLower_00_Skeleton.rpt" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidLower_00_Skeleton.r" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidLower_00_Skeleton.ro" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidLower_00_Skeleton.s" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidLower_00_Skeleton.pm" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidLower_00_Skeleton.jo" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidLower_00_Skeleton.ssc" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidLower_00_Skeleton.is" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP.pim" "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidLower_00_Skeleton.s" "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidLower_00_Skeleton.pm" "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidLower_01_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LidLower_01_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidLower_01_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LidLower_01_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LidLower_01_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LidLower_01_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidLower_01_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidLower_01_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidLower_01_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP.ro" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP.pim" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP.rp" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP.rpt" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidLower_01_Skeleton.t" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidLower_01_Skeleton.rp" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidLower_01_Skeleton.rpt" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidLower_01_Skeleton.r" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidLower_01_Skeleton.ro" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidLower_01_Skeleton.s" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidLower_01_Skeleton.pm" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidLower_01_Skeleton.jo" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidLower_01_Skeleton.ssc" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidLower_01_Skeleton.is" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP.pim" "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidLower_01_Skeleton.s" "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidLower_01_Skeleton.pm" "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidLower_02_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LidLower_02_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidLower_02_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LidLower_02_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LidLower_02_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LidLower_02_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidLower_02_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidLower_02_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidLower_02_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP.ro" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP.pim" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP.rp" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP.rpt" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidLower_02_Skeleton.t" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidLower_02_Skeleton.rp" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidLower_02_Skeleton.rpt" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidLower_02_Skeleton.r" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidLower_02_Skeleton.ro" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidLower_02_Skeleton.s" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidLower_02_Skeleton.pm" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidLower_02_Skeleton.jo" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidLower_02_Skeleton.ssc" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidLower_02_Skeleton.is" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP.pim" "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidLower_02_Skeleton.s" "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidLower_02_Skeleton.pm" "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketUpper_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketUpper_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketUpper_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketUpper_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketUpper_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketUpper_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketUpper_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketUpper_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketUpper_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP.ro" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP.pim" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP.rp" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP.rpt" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketUpper_00_Skeleton.t" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketUpper_00_Skeleton.rp" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketUpper_00_Skeleton.rpt" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketUpper_00_Skeleton.r" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketUpper_00_Skeleton.ro" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketUpper_00_Skeleton.s" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketUpper_00_Skeleton.pm" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketUpper_00_Skeleton.jo" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketUpper_00_Skeleton.ssc" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketUpper_00_Skeleton.is" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP.pim" "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketUpper_00_Skeleton.s" "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketUpper_00_Skeleton.pm" "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketUpper_01_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketUpper_01_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketUpper_01_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketUpper_01_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketUpper_01_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketUpper_01_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketUpper_01_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketUpper_01_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketUpper_01_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP.ro" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP.pim" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP.rp" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP.rpt" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketUpper_01_Skeleton.t" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketUpper_01_Skeleton.rp" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketUpper_01_Skeleton.rpt" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketUpper_01_Skeleton.r" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketUpper_01_Skeleton.ro" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketUpper_01_Skeleton.s" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketUpper_01_Skeleton.pm" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketUpper_01_Skeleton.jo" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketUpper_01_Skeleton.ssc" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketUpper_01_Skeleton.is" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP.pim" "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketUpper_01_Skeleton.s" "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketUpper_01_Skeleton.pm" "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketUpper_02_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketUpper_02_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketUpper_02_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketUpper_02_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketUpper_02_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketUpper_02_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketUpper_02_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketUpper_02_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketUpper_02_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP.ro" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP.pim" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP.rp" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP.rpt" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketUpper_02_Skeleton.t" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketUpper_02_Skeleton.rp" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketUpper_02_Skeleton.rpt" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketUpper_02_Skeleton.r" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketUpper_02_Skeleton.ro" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketUpper_02_Skeleton.s" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketUpper_02_Skeleton.pm" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketUpper_02_Skeleton.jo" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketUpper_02_Skeleton.ssc" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketUpper_02_Skeleton.is" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP.pim" "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketUpper_02_Skeleton.s" "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketUpper_02_Skeleton.pm" "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketLower_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketLower_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketLower_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketLower_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketLower_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketLower_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketLower_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketLower_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketLower_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP.ro" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP.pim" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP.rp" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP.rpt" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketLower_02_Skeleton.t" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketLower_02_Skeleton.rp" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketLower_02_Skeleton.rpt" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketLower_02_Skeleton.r" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketLower_02_Skeleton.ro" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketLower_02_Skeleton.s" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketLower_02_Skeleton.pm" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketLower_02_Skeleton.jo" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketLower_02_Skeleton.ssc" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketLower_02_Skeleton.is" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP.pim" "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketLower_02_Skeleton.s" "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketLower_02_Skeleton.pm" "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketLower_01_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketLower_01_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketLower_01_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketLower_01_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketLower_01_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketLower_01_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketLower_01_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketLower_01_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketLower_01_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP.ro" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP.pim" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP.rp" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP.rpt" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketLower_01_Skeleton.t" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketLower_01_Skeleton.rp" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketLower_01_Skeleton.rpt" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketLower_01_Skeleton.r" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketLower_01_Skeleton.ro" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketLower_01_Skeleton.s" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketLower_01_Skeleton.pm" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketLower_01_Skeleton.jo" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketLower_01_Skeleton.ssc" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketLower_01_Skeleton.is" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP.pim" "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketLower_01_Skeleton.s" "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketLower_01_Skeleton.pm" "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketLower_02_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketLower_02_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketLower_02_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketLower_02_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketLower_02_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketLower_02_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketLower_02_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketLower_02_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketLower_02_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP.ro" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP.pim" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP.rp" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP.rpt" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketLower_00_Skeleton.t" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketLower_00_Skeleton.rp" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketLower_00_Skeleton.rpt" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketLower_00_Skeleton.r" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketLower_00_Skeleton.ro" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketLower_00_Skeleton.s" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketLower_00_Skeleton.pm" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketLower_00_Skeleton.jo" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketLower_00_Skeleton.ssc" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketLower_00_Skeleton.is" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP.pim" "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketLower_00_Skeleton.s" "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketLower_00_Skeleton.pm" "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidInner_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LidInner_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidInner_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LidInner_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LidInner_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LidInner_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidInner_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidInner_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidInner_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP.ro" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP.pim" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP.rp" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP.rpt" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidInner_00_Skeleton.t" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidInner_00_Skeleton.rp" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidInner_00_Skeleton.rpt" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidInner_00_Skeleton.r" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidInner_00_Skeleton.ro" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidInner_00_Skeleton.s" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidInner_00_Skeleton.pm" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidInner_00_Skeleton.jo" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidInner_00_Skeleton.ssc" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidInner_00_Skeleton.is" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP.pim" "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidInner_00_Skeleton.s" "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidInner_00_Skeleton.pm" "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_LidOuter_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_LidOuter_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_LidOuter_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_LidOuter_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_LidOuter_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_LidOuter_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_LidOuter_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_LidOuter_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_LidOuter_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP.ro" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP.pim" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP.rp" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP.rpt" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_LidOuter_00_Skeleton.t" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_LidOuter_00_Skeleton.rp" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_LidOuter_00_Skeleton.rpt" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_LidOuter_00_Skeleton.r" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_LidOuter_00_Skeleton.ro" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_LidOuter_00_Skeleton.s" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_LidOuter_00_Skeleton.pm" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_LidOuter_00_Skeleton.jo" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_LidOuter_00_Skeleton.ssc" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_LidOuter_00_Skeleton.is" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP.pim" "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_LidOuter_00_Skeleton.s" "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_LidOuter_00_Skeleton.pm" "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketInner_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketInner_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketInner_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketInner_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketInner_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketInner_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketInner_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketInner_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketInner_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP.ro" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP.pim" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP.rp" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP.rpt" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketInner_00_Skeleton.t" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketInner_00_Skeleton.rp" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketInner_00_Skeleton.rpt" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketInner_00_Skeleton.r" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketInner_00_Skeleton.ro" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketInner_00_Skeleton.s" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketInner_00_Skeleton.pm" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketInner_00_Skeleton.jo" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketInner_00_Skeleton.ssc" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketInner_00_Skeleton.is" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP.pim" "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketInner_00_Skeleton.s" "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketInner_00_Skeleton.pm" "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "L_SocketOuter_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "L_SocketOuter_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "L_SocketOuter_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "L_SocketOuter_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "L_SocketOuter_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "L_SocketOuter_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "L_SocketOuter_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "L_SocketOuter_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "L_SocketOuter_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP.ro" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP.pim" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP.rp" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP.rpt" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "L_SocketOuter_00_Skeleton.t" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "L_SocketOuter_00_Skeleton.rp" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "L_SocketOuter_00_Skeleton.rpt" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "L_SocketOuter_00_Skeleton.r" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "L_SocketOuter_00_Skeleton.ro" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "L_SocketOuter_00_Skeleton.s" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "L_SocketOuter_00_Skeleton.pm" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketOuter_00_Skeleton.jo" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "L_SocketOuter_00_Skeleton.ssc" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "L_SocketOuter_00_Skeleton.is" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "L_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP.pim" "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "L_SocketOuter_00_Skeleton.s" "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "L_SocketOuter_00_Skeleton.pm" "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "L_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidUpper_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LidUpper_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidUpper_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LidUpper_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LidUpper_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LidUpper_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidUpper_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidUpper_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidUpper_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP.ro" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP.pim" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP.rp" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP.rpt" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidUpper_00_Skeleton.t" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidUpper_00_Skeleton.rp" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidUpper_00_Skeleton.rpt" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidUpper_00_Skeleton.r" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidUpper_00_Skeleton.ro" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidUpper_00_Skeleton.s" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_00_Skeleton.pm" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_00_Skeleton.jo" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidUpper_00_Skeleton.ssc" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidUpper_00_Skeleton.is" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LidUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP.pim" "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidUpper_00_Skeleton.s" "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_00_Skeleton.pm" "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidUpper_01_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LidUpper_01_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidUpper_01_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LidUpper_01_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LidUpper_01_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LidUpper_01_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidUpper_01_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidUpper_01_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidUpper_01_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP.ro" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP.pim" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP.rp" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP.rpt" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidUpper_01_Skeleton.t" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidUpper_01_Skeleton.rp" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidUpper_01_Skeleton.rpt" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidUpper_01_Skeleton.r" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidUpper_01_Skeleton.ro" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidUpper_01_Skeleton.s" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_01_Skeleton.pm" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_01_Skeleton.jo" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidUpper_01_Skeleton.ssc" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidUpper_01_Skeleton.is" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LidUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP.pim" "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidUpper_01_Skeleton.s" "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_01_Skeleton.pm" "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidUpper_02_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LidUpper_02_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidUpper_02_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LidUpper_02_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LidUpper_02_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LidUpper_02_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidUpper_02_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidUpper_02_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidUpper_02_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP.ro" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP.pim" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP.rp" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP.rpt" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidUpper_02_Skeleton.t" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidUpper_02_Skeleton.rp" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidUpper_02_Skeleton.rpt" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidUpper_02_Skeleton.r" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidUpper_02_Skeleton.ro" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidUpper_02_Skeleton.s" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_02_Skeleton.pm" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_02_Skeleton.jo" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidUpper_02_Skeleton.ssc" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidUpper_02_Skeleton.is" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LidUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP.pim" "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidUpper_02_Skeleton.s" "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidUpper_02_Skeleton.pm" "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidLower_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LidLower_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidLower_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LidLower_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LidLower_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LidLower_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidLower_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidLower_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidLower_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP.ro" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP.pim" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP.rp" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP.rpt" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidLower_00_Skeleton.t" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidLower_00_Skeleton.rp" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidLower_00_Skeleton.rpt" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidLower_00_Skeleton.r" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidLower_00_Skeleton.ro" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidLower_00_Skeleton.s" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidLower_00_Skeleton.pm" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidLower_00_Skeleton.jo" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidLower_00_Skeleton.ssc" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidLower_00_Skeleton.is" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LidLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP.pim" "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidLower_00_Skeleton.s" "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidLower_00_Skeleton.pm" "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidLower_01_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LidLower_01_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidLower_01_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LidLower_01_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LidLower_01_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LidLower_01_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidLower_01_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidLower_01_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidLower_01_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP.ro" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP.pim" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP.rp" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP.rpt" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidLower_01_Skeleton.t" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidLower_01_Skeleton.rp" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidLower_01_Skeleton.rpt" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidLower_01_Skeleton.r" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidLower_01_Skeleton.ro" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidLower_01_Skeleton.s" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidLower_01_Skeleton.pm" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidLower_01_Skeleton.jo" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidLower_01_Skeleton.ssc" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidLower_01_Skeleton.is" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LidLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP.pim" "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidLower_01_Skeleton.s" "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidLower_01_Skeleton.pm" "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidLower_02_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LidLower_02_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidLower_02_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LidLower_02_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LidLower_02_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LidLower_02_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidLower_02_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidLower_02_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidLower_02_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP.ro" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP.pim" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP.rp" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP.rpt" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidLower_02_Skeleton.t" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidLower_02_Skeleton.rp" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidLower_02_Skeleton.rpt" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidLower_02_Skeleton.r" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidLower_02_Skeleton.ro" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidLower_02_Skeleton.s" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidLower_02_Skeleton.pm" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidLower_02_Skeleton.jo" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidLower_02_Skeleton.ssc" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidLower_02_Skeleton.is" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LidLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP.pim" "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidLower_02_Skeleton.s" "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidLower_02_Skeleton.pm" "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketUpper_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketUpper_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketUpper_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketUpper_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketUpper_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketUpper_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketUpper_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketUpper_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketUpper_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP.ro" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP.pim" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP.rp" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP.rpt" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketUpper_00_Skeleton.t" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketUpper_00_Skeleton.rp" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketUpper_00_Skeleton.rpt" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketUpper_00_Skeleton.r" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketUpper_00_Skeleton.ro" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketUpper_00_Skeleton.s" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketUpper_00_Skeleton.pm" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketUpper_00_Skeleton.jo" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketUpper_00_Skeleton.ssc" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketUpper_00_Skeleton.is" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketUpper_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP.pim" "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketUpper_00_Skeleton.s" "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketUpper_00_Skeleton.pm" "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketUpper_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketUpper_01_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketUpper_01_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketUpper_01_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketUpper_01_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketUpper_01_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketUpper_01_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketUpper_01_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketUpper_01_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketUpper_01_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP.ro" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP.pim" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP.rp" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP.rpt" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketUpper_01_Skeleton.t" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketUpper_01_Skeleton.rp" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketUpper_01_Skeleton.rpt" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketUpper_01_Skeleton.r" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketUpper_01_Skeleton.ro" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketUpper_01_Skeleton.s" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketUpper_01_Skeleton.pm" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketUpper_01_Skeleton.jo" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketUpper_01_Skeleton.ssc" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketUpper_01_Skeleton.is" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketUpper_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP.pim" "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketUpper_01_Skeleton.s" "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketUpper_01_Skeleton.pm" "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketUpper_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketUpper_02_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketUpper_02_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketUpper_02_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketUpper_02_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketUpper_02_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketUpper_02_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketUpper_02_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketUpper_02_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketUpper_02_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP.ro" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP.pim" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP.rp" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP.rpt" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketUpper_02_Skeleton.t" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketUpper_02_Skeleton.rp" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketUpper_02_Skeleton.rpt" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketUpper_02_Skeleton.r" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketUpper_02_Skeleton.ro" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketUpper_02_Skeleton.s" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketUpper_02_Skeleton.pm" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketUpper_02_Skeleton.jo" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketUpper_02_Skeleton.ssc" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketUpper_02_Skeleton.is" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketUpper_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP.pim" "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketUpper_02_Skeleton.s" "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketUpper_02_Skeleton.pm" "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketUpper_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketLower_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketLower_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketLower_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketLower_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketLower_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketLower_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketLower_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketLower_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketLower_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP.ro" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP.pim" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP.rp" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP.rpt" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketLower_02_Skeleton.t" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketLower_02_Skeleton.rp" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketLower_02_Skeleton.rpt" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketLower_02_Skeleton.r" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketLower_02_Skeleton.ro" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketLower_02_Skeleton.s" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketLower_02_Skeleton.pm" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketLower_02_Skeleton.jo" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketLower_02_Skeleton.ssc" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketLower_02_Skeleton.is" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketLower_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP.pim" "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketLower_02_Skeleton.s" "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketLower_02_Skeleton.pm" "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketLower_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketLower_01_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketLower_01_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketLower_01_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketLower_01_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketLower_01_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketLower_01_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketLower_01_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketLower_01_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketLower_01_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP.ro" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP.pim" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP.rp" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP.rpt" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketLower_01_Skeleton.t" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketLower_01_Skeleton.rp" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketLower_01_Skeleton.rpt" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketLower_01_Skeleton.r" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketLower_01_Skeleton.ro" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketLower_01_Skeleton.s" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketLower_01_Skeleton.pm" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketLower_01_Skeleton.jo" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketLower_01_Skeleton.ssc" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketLower_01_Skeleton.is" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketLower_01_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP.pim" "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketLower_01_Skeleton.s" "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketLower_01_Skeleton.pm" "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketLower_01_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketLower_02_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketLower_02_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketLower_02_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketLower_02_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketLower_02_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketLower_02_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketLower_02_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketLower_02_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketLower_02_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP.ro" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP.pim" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP.rp" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP.rpt" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketLower_00_Skeleton.t" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketLower_00_Skeleton.rp" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketLower_00_Skeleton.rpt" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketLower_00_Skeleton.r" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketLower_00_Skeleton.ro" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketLower_00_Skeleton.s" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketLower_00_Skeleton.pm" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketLower_00_Skeleton.jo" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketLower_00_Skeleton.ssc" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketLower_00_Skeleton.is" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketLower_02_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP.pim" "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketLower_00_Skeleton.s" "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketLower_00_Skeleton.pm" "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketLower_02_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidInner_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LidInner_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidInner_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LidInner_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LidInner_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LidInner_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidInner_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidInner_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidInner_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP.ro" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP.pim" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP.rp" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP.rpt" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidInner_00_Skeleton.t" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidInner_00_Skeleton.rp" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidInner_00_Skeleton.rpt" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidInner_00_Skeleton.r" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidInner_00_Skeleton.ro" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidInner_00_Skeleton.s" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidInner_00_Skeleton.pm" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidInner_00_Skeleton.jo" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidInner_00_Skeleton.ssc" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidInner_00_Skeleton.is" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LidInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP.pim" "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidInner_00_Skeleton.s" "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidInner_00_Skeleton.pm" "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_LidOuter_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_LidOuter_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_LidOuter_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_LidOuter_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_LidOuter_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_LidOuter_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_LidOuter_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_LidOuter_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_LidOuter_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP.ro" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP.pim" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP.rp" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP.rpt" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_LidOuter_00_Skeleton.t" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_LidOuter_00_Skeleton.rp" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_LidOuter_00_Skeleton.rpt" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_LidOuter_00_Skeleton.r" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_LidOuter_00_Skeleton.ro" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_LidOuter_00_Skeleton.s" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_LidOuter_00_Skeleton.pm" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_LidOuter_00_Skeleton.jo" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_LidOuter_00_Skeleton.ssc" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_LidOuter_00_Skeleton.is" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_LidOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP.pim" "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_LidOuter_00_Skeleton.s" "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_LidOuter_00_Skeleton.pm" "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_LidOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketInner_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketInner_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketInner_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketInner_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketInner_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketInner_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketInner_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketInner_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketInner_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP.ro" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP.pim" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP.rp" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP.rpt" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketInner_00_Skeleton.t" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketInner_00_Skeleton.rp" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketInner_00_Skeleton.rpt" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketInner_00_Skeleton.r" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketInner_00_Skeleton.ro" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketInner_00_Skeleton.s" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketInner_00_Skeleton.pm" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketInner_00_Skeleton.jo" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketInner_00_Skeleton.ssc" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketInner_00_Skeleton.is" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketInner_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP.pim" "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketInner_00_Skeleton.s" "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketInner_00_Skeleton.pm" "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketInner_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctx" "R_SocketOuter_00_Part_CtrlPosition_GRP.tx"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cty" "R_SocketOuter_00_Part_CtrlPosition_GRP.ty"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.ctz" "R_SocketOuter_00_Part_CtrlPosition_GRP.tz"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crx" "R_SocketOuter_00_Part_CtrlPosition_GRP.rx"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cry" "R_SocketOuter_00_Part_CtrlPosition_GRP.ry"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crz" "R_SocketOuter_00_Part_CtrlPosition_GRP.rz"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csx" "R_SocketOuter_00_Part_CtrlPosition_GRP.sx"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csy" "R_SocketOuter_00_Part_CtrlPosition_GRP.sy"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.csz" "R_SocketOuter_00_Part_CtrlPosition_GRP.sz"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP.ro" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cro"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP.pim" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.cpim"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP.rp" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crp"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP.rpt" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.crt"
		;
connectAttr "R_SocketOuter_00_Skeleton.t" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "R_SocketOuter_00_Skeleton.rp" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "R_SocketOuter_00_Skeleton.rpt" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "R_SocketOuter_00_Skeleton.r" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "R_SocketOuter_00_Skeleton.ro" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "R_SocketOuter_00_Skeleton.s" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "R_SocketOuter_00_Skeleton.pm" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketOuter_00_Skeleton.jo" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tjo"
		;
connectAttr "R_SocketOuter_00_Skeleton.ssc" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tsc"
		;
connectAttr "R_SocketOuter_00_Skeleton.is" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tis"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.w0" "R_SocketOuter_00_Part_CtrlPosition_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP.pim" "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.cpim"
		;
connectAttr "R_SocketOuter_00_Skeleton.s" "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "R_SocketOuter_00_Skeleton.pm" "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.w0" "R_SocketOuter_00_Part_CtrlPosition_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "Facial_LatticeShapeOrig.wl" "Facial_LatticeShape.li";
connectAttr "LatticeJaw_00_LatticeLOC.s" "LatticeJaw_01_LatticeLOC.is";
connectAttr "LatticeJaw_01_LatticeLOC.s" "LatticeJaw_02_LatticeLOC.is";
connectAttr "LatticeMiddle_01_LatticeLOC.s" "LatticeUpper_00_LatticeLOC.is";
connectAttr "LatticeMiddle_01_LatticeLOC.s" "LatticeLower_00_LatticeLOC.is";
connectAttr "transformGeometry1.og" "Lattice_CVShape.cr";
connectAttr "skinCluster1GroupId.id" "Brow_cvShape.iog.og[10].gid";
connectAttr "skinCluster1Set.mwc" "Brow_cvShape.iog.og[10].gco";
connectAttr "HelpNodes_skinCluster1.og[0]" "Brow_cvShape.cr";
connectAttr "skinCluster3GroupId.id" "L_Socket_cvShape.iog.og[4].gid";
connectAttr "skinCluster3Set.mwc" "L_Socket_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster3.og[0]" "L_Socket_cvShape.cr";
connectAttr "skinCluster2GroupId.id" "L_Lid_cvShape.iog.og[4].gid";
connectAttr "skinCluster2Set.mwc" "L_Lid_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster2.og[0]" "L_Lid_cvShape.cr";
connectAttr "skinCluster4GroupId.id" "R_Socket_cvShape.iog.og[4].gid";
connectAttr "skinCluster4Set.mwc" "R_Socket_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster4.og[0]" "R_Socket_cvShape.cr";
connectAttr "skinCluster5GroupId.id" "R_Lid_cvShape.iog.og[4].gid";
connectAttr "skinCluster5Set.mwc" "R_Lid_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster5.og[0]" "R_Lid_cvShape.cr";
connectAttr "skinCluster6GroupId.id" "L_Orbit_cvShape.iog.og[4].gid";
connectAttr "skinCluster6Set.mwc" "L_Orbit_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster6.og[0]" "L_Orbit_cvShape.cr";
connectAttr "skinCluster7GroupId.id" "R_Orbit_cvShape.iog.og[4].gid";
connectAttr "skinCluster7Set.mwc" "R_Orbit_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster7.og[0]" "R_Orbit_cvShape.cr";
connectAttr "skinCluster8GroupId.id" "Mouth_cvShape.iog.og[4].gid";
connectAttr "skinCluster8Set.mwc" "Mouth_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster8.og[0]" "Mouth_cvShape.cr";
connectAttr "skinCluster9GroupId.id" "Lip_cvShape.iog.og[4].gid";
connectAttr "skinCluster9Set.mwc" "Lip_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster9.og[0]" "Lip_cvShape.cr";
connectAttr "skinCluster10GroupId.id" "JawLine_cvShape.iog.og[4].gid";
connectAttr "skinCluster10Set.mwc" "JawLine_cvShape.iog.og[4].gco";
connectAttr "HelpNodes_skinCluster10.og[0]" "JawLine_cvShape.cr";
connectAttr "skinCluster13.og[0]" "TeethUpper_cvShape.cr";
connectAttr "tweak3.pl[0].cp[0]" "TeethUpper_cvShape.twl";
connectAttr "skinCluster13GroupId.id" "TeethUpper_cvShape.iog.og[0].gid";
connectAttr "skinCluster13Set.mwc" "TeethUpper_cvShape.iog.og[0].gco";
connectAttr "groupId6.id" "TeethUpper_cvShape.iog.og[1].gid";
connectAttr "tweakSet3.mwc" "TeethUpper_cvShape.iog.og[1].gco";
connectAttr "skinCluster14.og[0]" "TeethLower_cvShape.cr";
connectAttr "tweak4.pl[0].cp[0]" "TeethLower_cvShape.twl";
connectAttr "skinCluster14GroupId.id" "TeethLower_cvShape.iog.og[0].gid";
connectAttr "skinCluster14Set.mwc" "TeethLower_cvShape.iog.og[0].gco";
connectAttr "groupId8.id" "TeethLower_cvShape.iog.og[1].gid";
connectAttr "tweakSet4.mwc" "TeethLower_cvShape.iog.og[1].gco";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":TurtleDefaultBakeLayer.idx" ":TurtleBakeLayerManager.bli[0]";
connectAttr ":TurtleRenderOptions.msg" ":TurtleDefaultBakeLayer.rset";
connectAttr "skinCluster1GroupId.msg" "skinCluster1Set.gn" -na;
connectAttr "Brow_cvShape.iog.og[10]" "skinCluster1Set.dsm" -na;
connectAttr "HelpNodes_skinCluster1.msg" "skinCluster1Set.ub[0]";
connectAttr "skinCluster1GroupParts.og" "HelpNodes_skinCluster1.ip[0].ig";
connectAttr "skinCluster1GroupId.id" "HelpNodes_skinCluster1.ip[0].gi";
connectAttr "M_Brow_00_Skeleton.wm" "HelpNodes_skinCluster1.ma[0]";
connectAttr "L_Brow_00_Skeleton.wm" "HelpNodes_skinCluster1.ma[1]";
connectAttr "L_Brow_01_Skeleton.wm" "HelpNodes_skinCluster1.ma[2]";
connectAttr "L_Brow_02_Skeleton.wm" "HelpNodes_skinCluster1.ma[3]";
connectAttr "L_Brow_03_Skeleton.wm" "HelpNodes_skinCluster1.ma[4]";
connectAttr "R_Brow_00_Skeleton.wm" "HelpNodes_skinCluster1.ma[26]";
connectAttr "R_Brow_01_Skeleton.wm" "HelpNodes_skinCluster1.ma[27]";
connectAttr "R_Brow_02_Skeleton.wm" "HelpNodes_skinCluster1.ma[28]";
connectAttr "R_Brow_03_Skeleton.wm" "HelpNodes_skinCluster1.ma[29]";
connectAttr "M_Brow_00_Skeleton.liw" "HelpNodes_skinCluster1.lw[0]";
connectAttr "L_Brow_00_Skeleton.liw" "HelpNodes_skinCluster1.lw[1]";
connectAttr "L_Brow_01_Skeleton.liw" "HelpNodes_skinCluster1.lw[2]";
connectAttr "L_Brow_02_Skeleton.liw" "HelpNodes_skinCluster1.lw[3]";
connectAttr "L_Brow_03_Skeleton.liw" "HelpNodes_skinCluster1.lw[4]";
connectAttr "R_Brow_00_Skeleton.liw" "HelpNodes_skinCluster1.lw[26]";
connectAttr "R_Brow_01_Skeleton.liw" "HelpNodes_skinCluster1.lw[27]";
connectAttr "R_Brow_02_Skeleton.liw" "HelpNodes_skinCluster1.lw[28]";
connectAttr "R_Brow_03_Skeleton.liw" "HelpNodes_skinCluster1.lw[29]";
connectAttr "M_Brow_00_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[0]";
connectAttr "L_Brow_00_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[1]";
connectAttr "L_Brow_01_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[2]";
connectAttr "L_Brow_02_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[3]";
connectAttr "L_Brow_03_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[4]";
connectAttr "R_Brow_00_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[26]";
connectAttr "R_Brow_01_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[27]";
connectAttr "R_Brow_02_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[28]";
connectAttr "R_Brow_03_Skeleton.obcc" "HelpNodes_skinCluster1.ifcl[29]";
connectAttr "Brow_cvShapeOrig.ws" "skinCluster1GroupParts.ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1GroupParts.gi";
connectAttr "skinCluster3GroupId.msg" "skinCluster3Set.gn" -na;
connectAttr "L_Socket_cvShape.iog.og[4]" "skinCluster3Set.dsm" -na;
connectAttr "HelpNodes_skinCluster3.msg" "skinCluster3Set.ub[0]";
connectAttr "skinCluster3GroupParts.og" "HelpNodes_skinCluster3.ip[0].ig";
connectAttr "skinCluster3GroupId.id" "HelpNodes_skinCluster3.ip[0].gi";
connectAttr "L_SocketInner_00_Skeleton.wm" "HelpNodes_skinCluster3.ma[6]";
connectAttr "L_SocketUpper_00_Skeleton.wm" "HelpNodes_skinCluster3.ma[7]";
connectAttr "L_SocketUpper_01_Skeleton.wm" "HelpNodes_skinCluster3.ma[8]";
connectAttr "L_SocketUpper_02_Skeleton.wm" "HelpNodes_skinCluster3.ma[9]";
connectAttr "L_SocketOuter_00_Skeleton.wm" "HelpNodes_skinCluster3.ma[10]";
connectAttr "L_SocketLower_00_Skeleton.wm" "HelpNodes_skinCluster3.ma[11]";
connectAttr "L_SocketLower_01_Skeleton.wm" "HelpNodes_skinCluster3.ma[12]";
connectAttr "L_SocketLower_02_Skeleton.wm" "HelpNodes_skinCluster3.ma[13]";
connectAttr "L_SocketInner_00_Skeleton.liw" "HelpNodes_skinCluster3.lw[6]";
connectAttr "L_SocketUpper_00_Skeleton.liw" "HelpNodes_skinCluster3.lw[7]";
connectAttr "L_SocketUpper_01_Skeleton.liw" "HelpNodes_skinCluster3.lw[8]";
connectAttr "L_SocketUpper_02_Skeleton.liw" "HelpNodes_skinCluster3.lw[9]";
connectAttr "L_SocketOuter_00_Skeleton.liw" "HelpNodes_skinCluster3.lw[10]";
connectAttr "L_SocketLower_00_Skeleton.liw" "HelpNodes_skinCluster3.lw[11]";
connectAttr "L_SocketLower_01_Skeleton.liw" "HelpNodes_skinCluster3.lw[12]";
connectAttr "L_SocketLower_02_Skeleton.liw" "HelpNodes_skinCluster3.lw[13]";
connectAttr "L_SocketInner_00_Skeleton.obcc" "HelpNodes_skinCluster3.ifcl[6]";
connectAttr "L_SocketUpper_00_Skeleton.obcc" "HelpNodes_skinCluster3.ifcl[7]";
connectAttr "L_SocketUpper_01_Skeleton.obcc" "HelpNodes_skinCluster3.ifcl[8]";
connectAttr "L_SocketUpper_02_Skeleton.obcc" "HelpNodes_skinCluster3.ifcl[9]";
connectAttr "L_SocketOuter_00_Skeleton.obcc" "HelpNodes_skinCluster3.ifcl[10]";
connectAttr "L_SocketLower_00_Skeleton.obcc" "HelpNodes_skinCluster3.ifcl[11]";
connectAttr "L_SocketLower_01_Skeleton.obcc" "HelpNodes_skinCluster3.ifcl[12]";
connectAttr "L_SocketLower_02_Skeleton.obcc" "HelpNodes_skinCluster3.ifcl[13]";
connectAttr "L_Socket_cvShapeOrig.ws" "skinCluster3GroupParts.ig";
connectAttr "skinCluster3GroupId.id" "skinCluster3GroupParts.gi";
connectAttr "skinCluster2GroupId.msg" "skinCluster2Set.gn" -na;
connectAttr "L_Lid_cvShape.iog.og[4]" "skinCluster2Set.dsm" -na;
connectAttr "HelpNodes_skinCluster2.msg" "skinCluster2Set.ub[0]";
connectAttr "skinCluster2GroupParts.og" "HelpNodes_skinCluster2.ip[0].ig";
connectAttr "skinCluster2GroupId.id" "HelpNodes_skinCluster2.ip[0].gi";
connectAttr "L_LidInner_00_Skeleton.wm" "HelpNodes_skinCluster2.ma[14]";
connectAttr "L_LidUpper_00_Skeleton.wm" "HelpNodes_skinCluster2.ma[15]";
connectAttr "L_LidUpper_01_Skeleton.wm" "HelpNodes_skinCluster2.ma[16]";
connectAttr "L_LidUpper_02_Skeleton.wm" "HelpNodes_skinCluster2.ma[17]";
connectAttr "L_LidOuter_00_Skeleton.wm" "HelpNodes_skinCluster2.ma[18]";
connectAttr "L_LidLower_00_Skeleton.wm" "HelpNodes_skinCluster2.ma[19]";
connectAttr "L_LidLower_01_Skeleton.wm" "HelpNodes_skinCluster2.ma[20]";
connectAttr "L_LidLower_02_Skeleton.wm" "HelpNodes_skinCluster2.ma[21]";
connectAttr "L_LidInner_00_Skeleton.liw" "HelpNodes_skinCluster2.lw[14]";
connectAttr "L_LidUpper_00_Skeleton.liw" "HelpNodes_skinCluster2.lw[15]";
connectAttr "L_LidUpper_01_Skeleton.liw" "HelpNodes_skinCluster2.lw[16]";
connectAttr "L_LidUpper_02_Skeleton.liw" "HelpNodes_skinCluster2.lw[17]";
connectAttr "L_LidOuter_00_Skeleton.liw" "HelpNodes_skinCluster2.lw[18]";
connectAttr "L_LidLower_00_Skeleton.liw" "HelpNodes_skinCluster2.lw[19]";
connectAttr "L_LidLower_01_Skeleton.liw" "HelpNodes_skinCluster2.lw[20]";
connectAttr "L_LidLower_02_Skeleton.liw" "HelpNodes_skinCluster2.lw[21]";
connectAttr "L_LidInner_00_Skeleton.obcc" "HelpNodes_skinCluster2.ifcl[14]";
connectAttr "L_LidUpper_00_Skeleton.obcc" "HelpNodes_skinCluster2.ifcl[15]";
connectAttr "L_LidUpper_01_Skeleton.obcc" "HelpNodes_skinCluster2.ifcl[16]";
connectAttr "L_LidUpper_02_Skeleton.obcc" "HelpNodes_skinCluster2.ifcl[17]";
connectAttr "L_LidOuter_00_Skeleton.obcc" "HelpNodes_skinCluster2.ifcl[18]";
connectAttr "L_LidLower_00_Skeleton.obcc" "HelpNodes_skinCluster2.ifcl[19]";
connectAttr "L_LidLower_01_Skeleton.obcc" "HelpNodes_skinCluster2.ifcl[20]";
connectAttr "L_LidLower_02_Skeleton.obcc" "HelpNodes_skinCluster2.ifcl[21]";
connectAttr "L_Lid_cvShapeOrig.ws" "skinCluster2GroupParts.ig";
connectAttr "skinCluster2GroupId.id" "skinCluster2GroupParts.gi";
connectAttr "skinCluster4GroupId.msg" "skinCluster4Set.gn" -na;
connectAttr "R_Socket_cvShape.iog.og[4]" "skinCluster4Set.dsm" -na;
connectAttr "HelpNodes_skinCluster4.msg" "skinCluster4Set.ub[0]";
connectAttr "skinCluster4GroupParts.og" "HelpNodes_skinCluster4.ip[0].ig";
connectAttr "skinCluster4GroupId.id" "HelpNodes_skinCluster4.ip[0].gi";
connectAttr "R_SocketInner_00_Skeleton.wm" "HelpNodes_skinCluster4.ma[42]";
connectAttr "R_SocketLower_00_Skeleton.wm" "HelpNodes_skinCluster4.ma[43]";
connectAttr "R_SocketLower_01_Skeleton.wm" "HelpNodes_skinCluster4.ma[44]";
connectAttr "R_SocketLower_02_Skeleton.wm" "HelpNodes_skinCluster4.ma[45]";
connectAttr "R_SocketOuter_00_Skeleton.wm" "HelpNodes_skinCluster4.ma[46]";
connectAttr "R_SocketUpper_00_Skeleton.wm" "HelpNodes_skinCluster4.ma[47]";
connectAttr "R_SocketUpper_01_Skeleton.wm" "HelpNodes_skinCluster4.ma[48]";
connectAttr "R_SocketUpper_02_Skeleton.wm" "HelpNodes_skinCluster4.ma[49]";
connectAttr "R_SocketInner_00_Skeleton.liw" "HelpNodes_skinCluster4.lw[42]";
connectAttr "R_SocketLower_00_Skeleton.liw" "HelpNodes_skinCluster4.lw[43]";
connectAttr "R_SocketLower_01_Skeleton.liw" "HelpNodes_skinCluster4.lw[44]";
connectAttr "R_SocketLower_02_Skeleton.liw" "HelpNodes_skinCluster4.lw[45]";
connectAttr "R_SocketOuter_00_Skeleton.liw" "HelpNodes_skinCluster4.lw[46]";
connectAttr "R_SocketUpper_00_Skeleton.liw" "HelpNodes_skinCluster4.lw[47]";
connectAttr "R_SocketUpper_01_Skeleton.liw" "HelpNodes_skinCluster4.lw[48]";
connectAttr "R_SocketUpper_02_Skeleton.liw" "HelpNodes_skinCluster4.lw[49]";
connectAttr "R_SocketInner_00_Skeleton.obcc" "HelpNodes_skinCluster4.ifcl[42]";
connectAttr "R_SocketLower_00_Skeleton.obcc" "HelpNodes_skinCluster4.ifcl[43]";
connectAttr "R_SocketLower_01_Skeleton.obcc" "HelpNodes_skinCluster4.ifcl[44]";
connectAttr "R_SocketLower_02_Skeleton.obcc" "HelpNodes_skinCluster4.ifcl[45]";
connectAttr "R_SocketOuter_00_Skeleton.obcc" "HelpNodes_skinCluster4.ifcl[46]";
connectAttr "R_SocketUpper_00_Skeleton.obcc" "HelpNodes_skinCluster4.ifcl[47]";
connectAttr "R_SocketUpper_01_Skeleton.obcc" "HelpNodes_skinCluster4.ifcl[48]";
connectAttr "R_SocketUpper_02_Skeleton.obcc" "HelpNodes_skinCluster4.ifcl[49]";
connectAttr "R_Socket_cvShapeOrig.ws" "skinCluster4GroupParts.ig";
connectAttr "skinCluster4GroupId.id" "skinCluster4GroupParts.gi";
connectAttr "skinCluster5GroupId.msg" "skinCluster5Set.gn" -na;
connectAttr "R_Lid_cvShape.iog.og[4]" "skinCluster5Set.dsm" -na;
connectAttr "HelpNodes_skinCluster5.msg" "skinCluster5Set.ub[0]";
connectAttr "skinCluster5GroupParts.og" "HelpNodes_skinCluster5.ip[0].ig";
connectAttr "skinCluster5GroupId.id" "HelpNodes_skinCluster5.ip[0].gi";
connectAttr "R_LidInner_00_Skeleton.wm" "HelpNodes_skinCluster5.ma[30]";
connectAttr "R_LidLower_00_Skeleton.wm" "HelpNodes_skinCluster5.ma[31]";
connectAttr "R_LidLower_01_Skeleton.wm" "HelpNodes_skinCluster5.ma[32]";
connectAttr "R_LidLower_02_Skeleton.wm" "HelpNodes_skinCluster5.ma[33]";
connectAttr "R_LidOuter_00_Skeleton.wm" "HelpNodes_skinCluster5.ma[34]";
connectAttr "R_LidUpper_00_Skeleton.wm" "HelpNodes_skinCluster5.ma[35]";
connectAttr "R_LidUpper_01_Skeleton.wm" "HelpNodes_skinCluster5.ma[36]";
connectAttr "R_LidUpper_02_Skeleton.wm" "HelpNodes_skinCluster5.ma[37]";
connectAttr "R_LidInner_00_Skeleton.liw" "HelpNodes_skinCluster5.lw[30]";
connectAttr "R_LidLower_00_Skeleton.liw" "HelpNodes_skinCluster5.lw[31]";
connectAttr "R_LidLower_01_Skeleton.liw" "HelpNodes_skinCluster5.lw[32]";
connectAttr "R_LidLower_02_Skeleton.liw" "HelpNodes_skinCluster5.lw[33]";
connectAttr "R_LidOuter_00_Skeleton.liw" "HelpNodes_skinCluster5.lw[34]";
connectAttr "R_LidUpper_00_Skeleton.liw" "HelpNodes_skinCluster5.lw[35]";
connectAttr "R_LidUpper_01_Skeleton.liw" "HelpNodes_skinCluster5.lw[36]";
connectAttr "R_LidUpper_02_Skeleton.liw" "HelpNodes_skinCluster5.lw[37]";
connectAttr "R_LidInner_00_Skeleton.obcc" "HelpNodes_skinCluster5.ifcl[30]";
connectAttr "R_LidLower_00_Skeleton.obcc" "HelpNodes_skinCluster5.ifcl[31]";
connectAttr "R_LidLower_01_Skeleton.obcc" "HelpNodes_skinCluster5.ifcl[32]";
connectAttr "R_LidLower_02_Skeleton.obcc" "HelpNodes_skinCluster5.ifcl[33]";
connectAttr "R_LidOuter_00_Skeleton.obcc" "HelpNodes_skinCluster5.ifcl[34]";
connectAttr "R_LidUpper_00_Skeleton.obcc" "HelpNodes_skinCluster5.ifcl[35]";
connectAttr "R_LidUpper_01_Skeleton.obcc" "HelpNodes_skinCluster5.ifcl[36]";
connectAttr "R_LidUpper_02_Skeleton.obcc" "HelpNodes_skinCluster5.ifcl[37]";
connectAttr "R_Lid_cvShapeOrig.ws" "skinCluster5GroupParts.ig";
connectAttr "skinCluster5GroupId.id" "skinCluster5GroupParts.gi";
connectAttr "skinCluster6GroupId.msg" "skinCluster6Set.gn" -na;
connectAttr "L_Orbit_cvShape.iog.og[4]" "skinCluster6Set.dsm" -na;
connectAttr "HelpNodes_skinCluster6.msg" "skinCluster6Set.ub[0]";
connectAttr "skinCluster6GroupParts.og" "HelpNodes_skinCluster6.ip[0].ig";
connectAttr "skinCluster6GroupId.id" "HelpNodes_skinCluster6.ip[0].gi";
connectAttr "L_Orbit_00_Skeleton.wm" "HelpNodes_skinCluster6.ma[22]";
connectAttr "L_Orbit_01_Skeleton.wm" "HelpNodes_skinCluster6.ma[23]";
connectAttr "L_Orbit_02_Skeleton.wm" "HelpNodes_skinCluster6.ma[24]";
connectAttr "L_Orbit_03_Skeleton.wm" "HelpNodes_skinCluster6.ma[25]";
connectAttr "L_Orbit_00_Skeleton.liw" "HelpNodes_skinCluster6.lw[22]";
connectAttr "L_Orbit_01_Skeleton.liw" "HelpNodes_skinCluster6.lw[23]";
connectAttr "L_Orbit_02_Skeleton.liw" "HelpNodes_skinCluster6.lw[24]";
connectAttr "L_Orbit_03_Skeleton.liw" "HelpNodes_skinCluster6.lw[25]";
connectAttr "L_Orbit_00_Skeleton.obcc" "HelpNodes_skinCluster6.ifcl[22]";
connectAttr "L_Orbit_01_Skeleton.obcc" "HelpNodes_skinCluster6.ifcl[23]";
connectAttr "L_Orbit_02_Skeleton.obcc" "HelpNodes_skinCluster6.ifcl[24]";
connectAttr "L_Orbit_03_Skeleton.obcc" "HelpNodes_skinCluster6.ifcl[25]";
connectAttr "L_Orbit_cvShapeOrig.ws" "skinCluster6GroupParts.ig";
connectAttr "skinCluster6GroupId.id" "skinCluster6GroupParts.gi";
connectAttr "skinCluster7GroupId.msg" "skinCluster7Set.gn" -na;
connectAttr "R_Orbit_cvShape.iog.og[4]" "skinCluster7Set.dsm" -na;
connectAttr "HelpNodes_skinCluster7.msg" "skinCluster7Set.ub[0]";
connectAttr "skinCluster7GroupParts.og" "HelpNodes_skinCluster7.ip[0].ig";
connectAttr "skinCluster7GroupId.id" "HelpNodes_skinCluster7.ip[0].gi";
connectAttr "R_Orbit_00_Skeleton.wm" "HelpNodes_skinCluster7.ma[38]";
connectAttr "R_Orbit_01_Skeleton.wm" "HelpNodes_skinCluster7.ma[39]";
connectAttr "R_Orbit_02_Skeleton.wm" "HelpNodes_skinCluster7.ma[40]";
connectAttr "R_Orbit_03_Skeleton.wm" "HelpNodes_skinCluster7.ma[41]";
connectAttr "R_Orbit_00_Skeleton.liw" "HelpNodes_skinCluster7.lw[38]";
connectAttr "R_Orbit_01_Skeleton.liw" "HelpNodes_skinCluster7.lw[39]";
connectAttr "R_Orbit_02_Skeleton.liw" "HelpNodes_skinCluster7.lw[40]";
connectAttr "R_Orbit_03_Skeleton.liw" "HelpNodes_skinCluster7.lw[41]";
connectAttr "R_Orbit_00_Skeleton.obcc" "HelpNodes_skinCluster7.ifcl[38]";
connectAttr "R_Orbit_01_Skeleton.obcc" "HelpNodes_skinCluster7.ifcl[39]";
connectAttr "R_Orbit_02_Skeleton.obcc" "HelpNodes_skinCluster7.ifcl[40]";
connectAttr "R_Orbit_03_Skeleton.obcc" "HelpNodes_skinCluster7.ifcl[41]";
connectAttr "R_Orbit_cvShapeOrig.ws" "skinCluster7GroupParts.ig";
connectAttr "skinCluster7GroupId.id" "skinCluster7GroupParts.gi";
connectAttr "skinCluster8GroupId.msg" "skinCluster8Set.gn" -na;
connectAttr "Mouth_cvShape.iog.og[4]" "skinCluster8Set.dsm" -na;
connectAttr "HelpNodes_skinCluster8.msg" "skinCluster8Set.ub[0]";
connectAttr "skinCluster8GroupParts.og" "HelpNodes_skinCluster8.ip[0].ig";
connectAttr "skinCluster8GroupId.id" "HelpNodes_skinCluster8.ip[0].gi";
connectAttr "L_MouthUpper_00_Skeleton.wm" "HelpNodes_skinCluster8.ma[50]";
connectAttr "R_MouthUpper_00_Skeleton.wm" "HelpNodes_skinCluster8.ma[51]";
connectAttr "L_MouthUpper_01_Skeleton.wm" "HelpNodes_skinCluster8.ma[52]";
connectAttr "R_MouthUpper_01_Skeleton.wm" "HelpNodes_skinCluster8.ma[53]";
connectAttr "L_MouthConner_00_Skeleton.wm" "HelpNodes_skinCluster8.ma[63]";
connectAttr "M_MouthLower_00_Skeleton.wm" "HelpNodes_skinCluster8.ma[64]";
connectAttr "L_MouthLower_00_Skeleton.wm" "HelpNodes_skinCluster8.ma[65]";
connectAttr "L_MouthLower_01_Skeleton.wm" "HelpNodes_skinCluster8.ma[66]";
connectAttr "R_MouthConner_00_Skeleton.wm" "HelpNodes_skinCluster8.ma[74]";
connectAttr "R_MouthLower_00_Skeleton.wm" "HelpNodes_skinCluster8.ma[75]";
connectAttr "R_MouthLower_01_Skeleton.wm" "HelpNodes_skinCluster8.ma[76]";
connectAttr "L_MouthUpper_00_Skeleton.liw" "HelpNodes_skinCluster8.lw[50]";
connectAttr "R_MouthUpper_00_Skeleton.liw" "HelpNodes_skinCluster8.lw[51]";
connectAttr "L_MouthUpper_01_Skeleton.liw" "HelpNodes_skinCluster8.lw[52]";
connectAttr "R_MouthUpper_01_Skeleton.liw" "HelpNodes_skinCluster8.lw[53]";
connectAttr "L_MouthConner_00_Skeleton.liw" "HelpNodes_skinCluster8.lw[63]";
connectAttr "M_MouthLower_00_Skeleton.liw" "HelpNodes_skinCluster8.lw[64]";
connectAttr "L_MouthLower_00_Skeleton.liw" "HelpNodes_skinCluster8.lw[65]";
connectAttr "L_MouthLower_01_Skeleton.liw" "HelpNodes_skinCluster8.lw[66]";
connectAttr "R_MouthConner_00_Skeleton.liw" "HelpNodes_skinCluster8.lw[74]";
connectAttr "R_MouthLower_00_Skeleton.liw" "HelpNodes_skinCluster8.lw[75]";
connectAttr "R_MouthLower_01_Skeleton.liw" "HelpNodes_skinCluster8.lw[76]";
connectAttr "L_MouthUpper_00_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[50]";
connectAttr "R_MouthUpper_00_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[51]";
connectAttr "L_MouthUpper_01_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[52]";
connectAttr "R_MouthUpper_01_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[53]";
connectAttr "L_MouthConner_00_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[63]";
connectAttr "M_MouthLower_00_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[64]";
connectAttr "L_MouthLower_00_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[65]";
connectAttr "L_MouthLower_01_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[66]";
connectAttr "R_MouthConner_00_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[74]";
connectAttr "R_MouthLower_00_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[75]";
connectAttr "R_MouthLower_01_Skeleton.obcc" "HelpNodes_skinCluster8.ifcl[76]";
connectAttr "Mouth_cvShapeOrig.ws" "skinCluster8GroupParts.ig";
connectAttr "skinCluster8GroupId.id" "skinCluster8GroupParts.gi";
connectAttr "skinCluster9GroupId.msg" "skinCluster9Set.gn" -na;
connectAttr "Lip_cvShape.iog.og[4]" "skinCluster9Set.dsm" -na;
connectAttr "HelpNodes_skinCluster9.msg" "skinCluster9Set.ub[0]";
connectAttr "skinCluster9GroupParts.og" "HelpNodes_skinCluster9.ip[0].ig";
connectAttr "skinCluster9GroupId.id" "HelpNodes_skinCluster9.ip[0].gi";
connectAttr "M_LipUpper_00_Skeleton.wm" "HelpNodes_skinCluster9.ma[54]";
connectAttr "L_LipUpper_00_Skeleton.wm" "HelpNodes_skinCluster9.ma[55]";
connectAttr "L_LipUpper_01_Skeleton.wm" "HelpNodes_skinCluster9.ma[56]";
connectAttr "L_LipUpper_02_Skeleton.wm" "HelpNodes_skinCluster9.ma[57]";
connectAttr "L_LipConner_00_Skeleton.wm" "HelpNodes_skinCluster9.ma[58]";
connectAttr "M_LipLower_00_Skeleton.wm" "HelpNodes_skinCluster9.ma[59]";
connectAttr "L_LipLower_00_Skeleton.wm" "HelpNodes_skinCluster9.ma[60]";
connectAttr "L_LipLower_01_Skeleton.wm" "HelpNodes_skinCluster9.ma[61]";
connectAttr "L_LipLower_02_Skeleton.wm" "HelpNodes_skinCluster9.ma[62]";
connectAttr "R_LipLower_00_Skeleton.wm" "HelpNodes_skinCluster9.ma[67]";
connectAttr "R_LipLower_01_Skeleton.wm" "HelpNodes_skinCluster9.ma[68]";
connectAttr "R_LipLower_02_Skeleton.wm" "HelpNodes_skinCluster9.ma[69]";
connectAttr "R_LipConner_00_Skeleton.wm" "HelpNodes_skinCluster9.ma[70]";
connectAttr "R_LipUpper_00_Skeleton.wm" "HelpNodes_skinCluster9.ma[71]";
connectAttr "R_LipUpper_01_Skeleton.wm" "HelpNodes_skinCluster9.ma[72]";
connectAttr "R_LipUpper_02_Skeleton.wm" "HelpNodes_skinCluster9.ma[73]";
connectAttr "M_LipUpper_00_Skeleton.liw" "HelpNodes_skinCluster9.lw[54]";
connectAttr "L_LipUpper_00_Skeleton.liw" "HelpNodes_skinCluster9.lw[55]";
connectAttr "L_LipUpper_01_Skeleton.liw" "HelpNodes_skinCluster9.lw[56]";
connectAttr "L_LipUpper_02_Skeleton.liw" "HelpNodes_skinCluster9.lw[57]";
connectAttr "L_LipConner_00_Skeleton.liw" "HelpNodes_skinCluster9.lw[58]";
connectAttr "M_LipLower_00_Skeleton.liw" "HelpNodes_skinCluster9.lw[59]";
connectAttr "L_LipLower_00_Skeleton.liw" "HelpNodes_skinCluster9.lw[60]";
connectAttr "L_LipLower_01_Skeleton.liw" "HelpNodes_skinCluster9.lw[61]";
connectAttr "L_LipLower_02_Skeleton.liw" "HelpNodes_skinCluster9.lw[62]";
connectAttr "R_LipLower_00_Skeleton.liw" "HelpNodes_skinCluster9.lw[67]";
connectAttr "R_LipLower_01_Skeleton.liw" "HelpNodes_skinCluster9.lw[68]";
connectAttr "R_LipLower_02_Skeleton.liw" "HelpNodes_skinCluster9.lw[69]";
connectAttr "R_LipConner_00_Skeleton.liw" "HelpNodes_skinCluster9.lw[70]";
connectAttr "R_LipUpper_00_Skeleton.liw" "HelpNodes_skinCluster9.lw[71]";
connectAttr "R_LipUpper_01_Skeleton.liw" "HelpNodes_skinCluster9.lw[72]";
connectAttr "R_LipUpper_02_Skeleton.liw" "HelpNodes_skinCluster9.lw[73]";
connectAttr "M_LipUpper_00_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[54]";
connectAttr "L_LipUpper_00_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[55]";
connectAttr "L_LipUpper_01_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[56]";
connectAttr "L_LipUpper_02_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[57]";
connectAttr "L_LipConner_00_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[58]";
connectAttr "M_LipLower_00_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[59]";
connectAttr "L_LipLower_00_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[60]";
connectAttr "L_LipLower_01_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[61]";
connectAttr "L_LipLower_02_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[62]";
connectAttr "R_LipLower_00_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[67]";
connectAttr "R_LipLower_01_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[68]";
connectAttr "R_LipLower_02_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[69]";
connectAttr "R_LipConner_00_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[70]";
connectAttr "R_LipUpper_00_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[71]";
connectAttr "R_LipUpper_01_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[72]";
connectAttr "R_LipUpper_02_Skeleton.obcc" "HelpNodes_skinCluster9.ifcl[73]";
connectAttr "Lip_cvShapeOrig.ws" "skinCluster9GroupParts.ig";
connectAttr "skinCluster9GroupId.id" "skinCluster9GroupParts.gi";
connectAttr "skinCluster10GroupId.msg" "skinCluster10Set.gn" -na;
connectAttr "JawLine_cvShape.iog.og[4]" "skinCluster10Set.dsm" -na;
connectAttr "HelpNodes_skinCluster10.msg" "skinCluster10Set.ub[0]";
connectAttr "skinCluster10GroupParts.og" "HelpNodes_skinCluster10.ip[0].ig";
connectAttr "skinCluster10GroupId.id" "HelpNodes_skinCluster10.ip[0].gi";
connectAttr "L_JawLine_02_Skeleton.wm" "HelpNodes_skinCluster10.ma[77]";
connectAttr "L_JawLine_01_Skeleton.wm" "HelpNodes_skinCluster10.ma[78]";
connectAttr "L_JawLine_00_Skeleton.wm" "HelpNodes_skinCluster10.ma[79]";
connectAttr "R_JawLine_00_Skeleton.wm" "HelpNodes_skinCluster10.ma[80]";
connectAttr "R_JawLine_01_Skeleton.wm" "HelpNodes_skinCluster10.ma[81]";
connectAttr "R_JawLine_02_Skeleton.wm" "HelpNodes_skinCluster10.ma[82]";
connectAttr "M_Chin_00_Skeleton.wm" "HelpNodes_skinCluster10.ma[83]";
connectAttr "L_JawLine_02_Skeleton.liw" "HelpNodes_skinCluster10.lw[77]";
connectAttr "L_JawLine_01_Skeleton.liw" "HelpNodes_skinCluster10.lw[78]";
connectAttr "L_JawLine_00_Skeleton.liw" "HelpNodes_skinCluster10.lw[79]";
connectAttr "R_JawLine_00_Skeleton.liw" "HelpNodes_skinCluster10.lw[80]";
connectAttr "R_JawLine_01_Skeleton.liw" "HelpNodes_skinCluster10.lw[81]";
connectAttr "R_JawLine_02_Skeleton.liw" "HelpNodes_skinCluster10.lw[82]";
connectAttr "M_Chin_00_Skeleton.liw" "HelpNodes_skinCluster10.lw[83]";
connectAttr "L_JawLine_02_Skeleton.obcc" "HelpNodes_skinCluster10.ifcl[77]";
connectAttr "L_JawLine_01_Skeleton.obcc" "HelpNodes_skinCluster10.ifcl[78]";
connectAttr "L_JawLine_00_Skeleton.obcc" "HelpNodes_skinCluster10.ifcl[79]";
connectAttr "R_JawLine_00_Skeleton.obcc" "HelpNodes_skinCluster10.ifcl[80]";
connectAttr "R_JawLine_01_Skeleton.obcc" "HelpNodes_skinCluster10.ifcl[81]";
connectAttr "R_JawLine_02_Skeleton.obcc" "HelpNodes_skinCluster10.ifcl[82]";
connectAttr "M_Chin_00_Skeleton.obcc" "HelpNodes_skinCluster10.ifcl[83]";
connectAttr "JawLine_cvShapeOrig.ws" "skinCluster10GroupParts.ig";
connectAttr "skinCluster10GroupId.id" "skinCluster10GroupParts.gi";
connectAttr "Facial_LatticeShape.wm" "Facial_LatticeFFD.dlm";
connectAttr "Facial_LatticeShape.lo" "Facial_LatticeFFD.dlp";
connectAttr "Facial_LatticeBaseShape.wm" "Facial_LatticeFFD.blm";
connectAttr "Facial_LatticeFFD.msg" "Facial_LatticeSet.ub[0]";
connectAttr "makeNurbCircle1.oc" "transformGeometry1.ig";
connectAttr "skinCluster13GroupParts.og" "skinCluster13.ip[0].ig";
connectAttr "skinCluster13GroupId.id" "skinCluster13.ip[0].gi";
connectAttr "bindPose3.msg" "skinCluster13.bp";
connectAttr "L_TeethUpper_Sec_02_Skeleton.wm" "skinCluster13.ma[0]";
connectAttr "L_TeethUpper_Sec_01_Skeleton.wm" "skinCluster13.ma[1]";
connectAttr "L_TeethUpper_Sec_00_Skeleton.wm" "skinCluster13.ma[2]";
connectAttr "M_TeethUpper_Sec_00_Skeleton.wm" "skinCluster13.ma[3]";
connectAttr "R_TeethUpper_Sec_00_Skeleton.wm" "skinCluster13.ma[4]";
connectAttr "R_TeethUpper_Sec_01_Skeleton.wm" "skinCluster13.ma[5]";
connectAttr "R_TeethUpper_Sec_02_Skeleton.wm" "skinCluster13.ma[6]";
connectAttr "L_TeethUpper_Sec_02_Skeleton.liw" "skinCluster13.lw[0]";
connectAttr "L_TeethUpper_Sec_01_Skeleton.liw" "skinCluster13.lw[1]";
connectAttr "L_TeethUpper_Sec_00_Skeleton.liw" "skinCluster13.lw[2]";
connectAttr "M_TeethUpper_Sec_00_Skeleton.liw" "skinCluster13.lw[3]";
connectAttr "R_TeethUpper_Sec_00_Skeleton.liw" "skinCluster13.lw[4]";
connectAttr "R_TeethUpper_Sec_01_Skeleton.liw" "skinCluster13.lw[5]";
connectAttr "R_TeethUpper_Sec_02_Skeleton.liw" "skinCluster13.lw[6]";
connectAttr "L_TeethUpper_Sec_02_Skeleton.obcc" "skinCluster13.ifcl[0]";
connectAttr "L_TeethUpper_Sec_01_Skeleton.obcc" "skinCluster13.ifcl[1]";
connectAttr "L_TeethUpper_Sec_00_Skeleton.obcc" "skinCluster13.ifcl[2]";
connectAttr "M_TeethUpper_Sec_00_Skeleton.obcc" "skinCluster13.ifcl[3]";
connectAttr "R_TeethUpper_Sec_00_Skeleton.obcc" "skinCluster13.ifcl[4]";
connectAttr "R_TeethUpper_Sec_01_Skeleton.obcc" "skinCluster13.ifcl[5]";
connectAttr "R_TeethUpper_Sec_02_Skeleton.obcc" "skinCluster13.ifcl[6]";
connectAttr "groupParts6.og" "tweak3.ip[0].ig";
connectAttr "groupId6.id" "tweak3.ip[0].gi";
connectAttr "skinCluster13GroupId.msg" "skinCluster13Set.gn" -na;
connectAttr "TeethUpper_cvShape.iog.og[0]" "skinCluster13Set.dsm" -na;
connectAttr "skinCluster13.msg" "skinCluster13Set.ub[0]";
connectAttr "tweak3.og[0]" "skinCluster13GroupParts.ig";
connectAttr "skinCluster13GroupId.id" "skinCluster13GroupParts.gi";
connectAttr "groupId6.msg" "tweakSet3.gn" -na;
connectAttr "TeethUpper_cvShape.iog.og[1]" "tweakSet3.dsm" -na;
connectAttr "tweak3.msg" "tweakSet3.ub[0]";
connectAttr "TeethUpper_cvShapeOrig.ws" "groupParts6.ig";
connectAttr "groupId6.id" "groupParts6.gi";
connectAttr "Facial_Skeleton_GRP.msg" "bindPose3.m[0]";
connectAttr "M_Head_Position.msg" "bindPose3.m[1]";
connectAttr "M_Head_Skeleton.msg" "bindPose3.m[2]";
connectAttr "M_HeadLower_Skeleton.msg" "bindPose3.m[3]";
connectAttr "HeadLower_Skeleton_GRP.msg" "bindPose3.m[4]";
connectAttr "HeadLower_None_GRP.msg" "bindPose3.m[5]";
connectAttr "TeethUpper_Second_GRP.msg" "bindPose3.m[6]";
connectAttr "L_TeethUpper_Sec_02_Skeleton.msg" "bindPose3.m[7]";
connectAttr "L_TeethUpper_Sec_01_Skeleton.msg" "bindPose3.m[8]";
connectAttr "L_TeethUpper_Sec_00_Skeleton.msg" "bindPose3.m[9]";
connectAttr "M_TeethUpper_Sec_00_Skeleton.msg" "bindPose3.m[10]";
connectAttr "R_TeethUpper_Sec_00_Skeleton.msg" "bindPose3.m[11]";
connectAttr "R_TeethUpper_Sec_01_Skeleton.msg" "bindPose3.m[12]";
connectAttr "R_TeethUpper_Sec_02_Skeleton.msg" "bindPose3.m[13]";
connectAttr "bindPose3.w" "bindPose3.p[0]";
connectAttr "bindPose3.m[0]" "bindPose3.p[1]";
connectAttr "bindPose3.m[1]" "bindPose3.p[2]";
connectAttr "bindPose3.m[2]" "bindPose3.p[3]";
connectAttr "bindPose3.m[3]" "bindPose3.p[4]";
connectAttr "bindPose3.m[4]" "bindPose3.p[5]";
connectAttr "bindPose3.m[5]" "bindPose3.p[6]";
connectAttr "bindPose3.m[6]" "bindPose3.p[7]";
connectAttr "bindPose3.m[6]" "bindPose3.p[8]";
connectAttr "bindPose3.m[6]" "bindPose3.p[9]";
connectAttr "bindPose3.m[6]" "bindPose3.p[10]";
connectAttr "bindPose3.m[6]" "bindPose3.p[11]";
connectAttr "bindPose3.m[6]" "bindPose3.p[12]";
connectAttr "bindPose3.m[6]" "bindPose3.p[13]";
connectAttr "M_Head_Skeleton.bps" "bindPose3.wm[2]";
connectAttr "M_HeadLower_Skeleton.bps" "bindPose3.wm[3]";
connectAttr "L_TeethUpper_Sec_02_Skeleton.bps" "bindPose3.wm[7]";
connectAttr "L_TeethUpper_Sec_01_Skeleton.bps" "bindPose3.wm[8]";
connectAttr "L_TeethUpper_Sec_00_Skeleton.bps" "bindPose3.wm[9]";
connectAttr "M_TeethUpper_Sec_00_Skeleton.bps" "bindPose3.wm[10]";
connectAttr "R_TeethUpper_Sec_00_Skeleton.bps" "bindPose3.wm[11]";
connectAttr "R_TeethUpper_Sec_01_Skeleton.bps" "bindPose3.wm[12]";
connectAttr "R_TeethUpper_Sec_02_Skeleton.bps" "bindPose3.wm[13]";
connectAttr "skinCluster14GroupParts.og" "skinCluster14.ip[0].ig";
connectAttr "skinCluster14GroupId.id" "skinCluster14.ip[0].gi";
connectAttr "bindPose4.msg" "skinCluster14.bp";
connectAttr "L_TeethLower_Sec_01_Skeleton1.wm" "skinCluster14.ma[0]";
connectAttr "L_TeethLower_Sec_01_Skeleton.wm" "skinCluster14.ma[1]";
connectAttr "L_TeethLower_Sec_00_Skeleton.wm" "skinCluster14.ma[2]";
connectAttr "M_TeethLower_Sec_00_Skeleton.wm" "skinCluster14.ma[3]";
connectAttr "R_TeethLower_Sec_00_Skeleton.wm" "skinCluster14.ma[4]";
connectAttr "R_TeethLower_Sec_01_Skeleton.wm" "skinCluster14.ma[5]";
connectAttr "R_TeethLower_Sec_01_Skeleton1.wm" "skinCluster14.ma[6]";
connectAttr "L_TeethLower_Sec_01_Skeleton1.liw" "skinCluster14.lw[0]";
connectAttr "L_TeethLower_Sec_01_Skeleton.liw" "skinCluster14.lw[1]";
connectAttr "L_TeethLower_Sec_00_Skeleton.liw" "skinCluster14.lw[2]";
connectAttr "M_TeethLower_Sec_00_Skeleton.liw" "skinCluster14.lw[3]";
connectAttr "R_TeethLower_Sec_00_Skeleton.liw" "skinCluster14.lw[4]";
connectAttr "R_TeethLower_Sec_01_Skeleton.liw" "skinCluster14.lw[5]";
connectAttr "R_TeethLower_Sec_01_Skeleton1.liw" "skinCluster14.lw[6]";
connectAttr "L_TeethLower_Sec_01_Skeleton1.obcc" "skinCluster14.ifcl[0]";
connectAttr "L_TeethLower_Sec_01_Skeleton.obcc" "skinCluster14.ifcl[1]";
connectAttr "L_TeethLower_Sec_00_Skeleton.obcc" "skinCluster14.ifcl[2]";
connectAttr "M_TeethLower_Sec_00_Skeleton.obcc" "skinCluster14.ifcl[3]";
connectAttr "R_TeethLower_Sec_00_Skeleton.obcc" "skinCluster14.ifcl[4]";
connectAttr "R_TeethLower_Sec_01_Skeleton.obcc" "skinCluster14.ifcl[5]";
connectAttr "R_TeethLower_Sec_01_Skeleton1.obcc" "skinCluster14.ifcl[6]";
connectAttr "groupParts8.og" "tweak4.ip[0].ig";
connectAttr "groupId8.id" "tweak4.ip[0].gi";
connectAttr "skinCluster14GroupId.msg" "skinCluster14Set.gn" -na;
connectAttr "TeethLower_cvShape.iog.og[0]" "skinCluster14Set.dsm" -na;
connectAttr "skinCluster14.msg" "skinCluster14Set.ub[0]";
connectAttr "tweak4.og[0]" "skinCluster14GroupParts.ig";
connectAttr "skinCluster14GroupId.id" "skinCluster14GroupParts.gi";
connectAttr "groupId8.msg" "tweakSet4.gn" -na;
connectAttr "TeethLower_cvShape.iog.og[1]" "tweakSet4.dsm" -na;
connectAttr "tweak4.msg" "tweakSet4.ub[0]";
connectAttr "TeethLower_cvShapeOrig.ws" "groupParts8.ig";
connectAttr "groupId8.id" "groupParts8.gi";
connectAttr "Facial_Skeleton_GRP.msg" "bindPose4.m[0]";
connectAttr "M_Head_Position.msg" "bindPose4.m[1]";
connectAttr "M_Head_Skeleton.msg" "bindPose4.m[2]";
connectAttr "M_HeadLower_Skeleton.msg" "bindPose4.m[3]";
connectAttr "HeadLower_Skeleton_GRP.msg" "bindPose4.m[4]";
connectAttr "HeadLower_None_GRP.msg" "bindPose4.m[5]";
connectAttr "TeethLower_Second_GRP.msg" "bindPose4.m[6]";
connectAttr "L_TeethLower_Sec_01_Skeleton1.msg" "bindPose4.m[7]";
connectAttr "L_TeethLower_Sec_01_Skeleton.msg" "bindPose4.m[8]";
connectAttr "L_TeethLower_Sec_00_Skeleton.msg" "bindPose4.m[9]";
connectAttr "M_TeethLower_Sec_00_Skeleton.msg" "bindPose4.m[10]";
connectAttr "R_TeethLower_Sec_00_Skeleton.msg" "bindPose4.m[11]";
connectAttr "R_TeethLower_Sec_01_Skeleton.msg" "bindPose4.m[12]";
connectAttr "R_TeethLower_Sec_01_Skeleton1.msg" "bindPose4.m[13]";
connectAttr "bindPose4.w" "bindPose4.p[0]";
connectAttr "bindPose4.m[0]" "bindPose4.p[1]";
connectAttr "bindPose4.m[1]" "bindPose4.p[2]";
connectAttr "bindPose4.m[2]" "bindPose4.p[3]";
connectAttr "bindPose4.m[3]" "bindPose4.p[4]";
connectAttr "bindPose4.m[4]" "bindPose4.p[5]";
connectAttr "bindPose4.m[5]" "bindPose4.p[6]";
connectAttr "bindPose4.m[6]" "bindPose4.p[7]";
connectAttr "bindPose4.m[6]" "bindPose4.p[8]";
connectAttr "bindPose4.m[6]" "bindPose4.p[9]";
connectAttr "bindPose4.m[6]" "bindPose4.p[10]";
connectAttr "bindPose4.m[6]" "bindPose4.p[11]";
connectAttr "bindPose4.m[6]" "bindPose4.p[12]";
connectAttr "bindPose4.m[6]" "bindPose4.p[13]";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "M_TeethUpper_00_SkeletonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "M_TeethLower_00_SkeletonShape.iog" ":initialShadingGroup.dsm" -na;
// End of fit_sh.ma
