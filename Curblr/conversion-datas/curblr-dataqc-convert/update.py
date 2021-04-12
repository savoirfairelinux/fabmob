import os
'''
ERROR MESSAGE:
////
    generate curblr... /home/eanoh/Bureau/CurbLr/conversion-mt-qc-et-map/curblr-dataqc-convert/segment_to_curblr.js:45
        if(rpaCode[TYPE_CODE].regulations){
                            ^

    TypeError: Cannot read property 'regulations' of undefined
        at Object.<anonymous> (/home/eanoh/Bureau/CurbLr/conversion-mt-qc-et-map/curblr-dataqc-convert/segment_to_curblr.js:45:27)
        at Module._compile (internal/modules/cjs/loader.js:777:30)
        at Object.Module._extensions..js (internal/modules/cjs/loader.js:788:10)
        at Module.load (internal/modules/cjs/loader.js:643:32)
        at Function.Module._load (internal/modules/cjs/loader.js:556:12)
        at Function.Module.runMain (internal/modules/cjs/loader.js:840:10)
        at internal/main/run_main_module.js:17:11
    done with that
////

files_to_inspect = [
    "vdq-panneauxstationnement-filtred-cap-rouge.geojson", # 0 octets a la fin
    "vdq-panneauxstationnement-filtred-cité-universitaire.geojson", # 0 octets a la fin
    "vdq-panneauxstationnement-filtred-lairet.geojson", # 0 octets a la fin
    "vdq-panneauxstationnement-filtred-quartier-4-5.geojson", # 0 octets a la fin
    "vdq-panneauxstationnement-filtred-quartier-5-4.geojson", # 0 octets a la fin
    "vdq-panneauxstationnement-filtred-saint-jean-baptiste.geojson", # 0 octets a la fin
    "vdq-panneauxstationnement-filtred-sillery.geojson", # 0 octets a la fin
    "vdq-panneauxstationnement-filtred-vieux-limoilou.geojson", 
]

ERROR MESSAGE
////
vdq-panneauxstationnement-filtred-l'aéroport.geojson
sh: 1: Syntax error: Unterminated quoted string
done created subset
generate curblr... sh: 1: Syntax error: Unterminated quoted string
sh: 1: Syntax error: Unterminated quoted string
'''
files = [
    # "vdq-panneauxstationnement-filtred-cap-rouge.geojson", # 0 octets a la fin
"vdq-panneauxstationnement-filtred-chutes-montmorency.geojson",
# "vdq-panneauxstationnement-filtred-cité-universitaire.geojson", # 0 octets a la fin
"vdq-panneauxstationnement-filtred-des-châtels.geojson",
"vdq-panneauxstationnement-filtred-duberger—les-saules.geojson",
"vdq-panneauxstationnement-filtred-jésuites.geojson",
"vdq-panneauxstationnement-filtred-lac-saint-charles.geojson",
# "vdq-panneauxstationnement-filtred-l-aéroport.geojson", #0 octets a la fin sh: 1: Syntax error: Unterminated quoted string
# "vdq-panneauxstationnement-filtred-lairet.geojson", # 0 octets a la fin
"vdq-panneauxstationnement-filtred-maizerets.geojson",
"vdq-panneauxstationnement-filtred-montcalm.geojson",
"vdq-panneauxstationnement-filtred-neufchatel-est—lebourgneuf.geojson",
"vdq-panneauxstationnement-filtred-notre-dame-des-laurentides.geojson",
"vdq-panneauxstationnement-filtred-plateau.geojson",
"vdq-panneauxstationnement-filtred-pointe-de-sainte-foy.geojson",
"vdq-panneauxstationnement-filtred-quartier-4-2.geojson",
"vdq-panneauxstationnement-filtred-quartier-4-3.geojson",
# "vdq-panneauxstationnement-filtred-quartier-4-5.geojson", # 0 octets a la fin
"vdq-panneauxstationnement-filtred-quartier-4-6.geojson",
"vdq-panneauxstationnement-filtred-quartier-5-1.geojson",
"vdq-panneauxstationnement-filtred-quartier-5-2.geojson",
# "vdq-panneauxstationnement-filtred-quartier-5-4.geojson", # 0 octets a la fin
# "vdq-panneauxstationnement-filtred-saint-jean-baptiste.geojson", # 0 octets a la fin
"vdq-panneauxstationnement-filtred-saint-louis.geojson",
"vdq-panneauxstationnement-filtred-saint-roch.geojson",
"vdq-panneauxstationnement-filtred-saint-sacrement.geojson",
"vdq-panneauxstationnement-filtred-saint-sauveur.geojson",
# "vdq-panneauxstationnement-filtred-sillery.geojson", # 0 octets a la fin
"vdq-panneauxstationnement-filtred-val-bélair.geojson",
"vdq-panneauxstationnement-filtred-vanier.geojson",
# "vdq-panneauxstationnement-filtred-vieux-limoilou.geojson", 
"vdq-panneauxstationnement-filtred-vieux-moulin.geojson",
"vdq-panneauxstationnement-filtred-vieux-québec—cap-blanc—colline-parlementaire.geojson"
]

os.system('echo -n "Retrieve online data... "')
os.system('wget -N -P data https://www.donneesquebec.ca/recherche/fr/dataset/9c11aab8-419c-4a7e-8bdc-95b5395a9f32/resource/27480cd1-ab19-47fe-a93b-9d526a0eb1e3/download/vdq-panneauxstationnement.geojson')
os.system('cp rpa/signalisation-codification-rpa.json data')
os.system('echo "done"')

#To be done instead of manual file')
#echo -n "create rpa... "')
#node vdq_to_rpa.js json > data/signalisation-codification-rpa.json')
#echo "done"')

os.system('echo -n "create regulations... "')
os.system('node rpa_to_regulations.js json > data/signalisation-codification-rpa_withRegulation.json')
os.system('echo "done"')

os.system('rm data/mtl-subset*')
os.system('echo -n "create subset... "')

for file in files:
    # file = files[17]
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", file)
    os.system('node subset.js data/' + file + ' > data/mtl-subset.geojson')
    os.system('echo "done created subset"')

    os.system('shst match data/mtl-subset.geojson --search-radius=15 --offset-line=10 --snap-side-of-street --buffer-points')

    os.system('echo -n "transform to segment... "')
    os.system('node mtl_to_segment.js > data/mtl-subset-segment.geojson')
    os.system('echo "done transform to segment"')

    os.system('shst match data/mtl-subset-segment.geojson --join-points --join-points-match-fields=TYPE_CODE \
        --search-radius=15 --snap-intersections --snap-intersections-radius=10 \
        --trim-intersections-radius=5 --buffer-merge-group-fields=ID \
        --buffer-points ')
        # --direction-field=direction --two-way-value=two --one-way-against-direction-value=against --one-way-with-direction-value=one


    os.system('echo -n "generate curblr... "')
    f_t_w = "data/" + file.replace(".geojson",".curblr.json")
    fd_t_m = "../../curb-map/src/assets/data/" 
    
    os.system('node segment_to_curblr.js > '+f_t_w)
    os.system('mv ' + f_t_w + " " + fd_t_m)
    os.system('echo "done with that"')

    #os.system('node stats.js > data/mtl-subset-unmanaged.geojson')

    os.system('date')
    # break