
D=/net/projects/EduPo

deploy_db:
	scp $D/data/new.db jardadupo:$D/data/

deploy_dicts:
	scp -r $D/tools/kveta/dicts $D/tools/kveta/trained_models jardadupo:$D/tools/kveta



