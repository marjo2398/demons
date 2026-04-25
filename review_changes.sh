# Let's verify we replaced correctly. We are looking for text-indigo and text-white.
echo "Remaining text-indigo in index.php:"
grep -oP 'text-indigo-\d+' index.php | sort | uniq -c

echo "Remaining text-white in index.php:"
grep -oP 'text-white(-\d+)?' index.php | sort | uniq -c

echo "Remaining text-indigo in host.php:"
grep -oP 'text-indigo-\d+' host.php | sort | uniq -c

echo "Remaining text-white in host.php:"
grep -oP 'text-white(-\d+)?' host.php | sort | uniq -c
