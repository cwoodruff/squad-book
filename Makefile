.PHONY: quiz cover epub html diagrams coverage manuscript links check validate clean
VOLS := vol1 vol2
quiz: ; python3 scripts/gen-quiz-appendix.py
epub: quiz ; for v in $(VOLS); do ./scripts/build.sh $$v epub || exit 1; done
html: quiz ; for v in $(VOLS); do ./scripts/build.sh $$v html || exit 1; done
diagrams: ; ./scripts/render-diagrams.sh
coverage: ; python3 scripts/check-coverage.py
links: ; ./scripts/check-links.sh
validate: epub ; for v in $(VOLS); do epubcheck dist/mastering-squad-$$v.epub || exit 1; done
manuscript: quiz ; python3 scripts/check-manuscript.py
check: coverage manuscript validate
clean: ; rm -rf dist
cover: ; ./scripts/render-cover.sh
