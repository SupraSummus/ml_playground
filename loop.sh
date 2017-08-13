mkdir -p log
while true; do
	make -j5 trainset
	make -j5 kill
	cat pool/*/score > log/`date +%s`
	make -j5 breed
done
