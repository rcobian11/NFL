import csv
import argparse
import scrapper
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    f.close()
    return i + 1

def first_part(site):
	site.write("<!--test nfl site -->\n"
				"<!DOCTYPE html>\n"
				"<html>\n"
				"<head>\n"
					"\t<title>NFL Picks</title>\n"
				"</head>\n"
				"<style>\n"
				"span {\n"
					"\tdisplay: inline-block;\n"
					"\twidth: 60px;\n"
					"\theight: 21px;\n"
				"}\n"
				"span_2 {\n"
					"\tdisplay: inline-block;\n"
					"\tbackground-color: rgb(200,200,200);\n"
				"}\n"
				"</style>\n"
				"<body>\n")


def form_check(site):
	picks = file_len('config.csv')
	site.write("<?php\n"
				"\t$name = '';\n"
				"\t$points = '';\n")
	for num1 in range(1, picks+1):
		site.write("\t$pick{} = '';\n".format(num1))
	site.write("\n\tif (isset($_POST['submit'])){\n"
		"\t\t$ok = true;\n")
	site.write("\t\tif(!isset($_POST['name']) || $_POST['name'] === ''){\n"
					"\t\t\t$ok = false;\n"
				"\t\t} else {\n"
					"\t\t\t$name = $_POST['name'];\n"
				"\t\t}\n\n")
	site.write("\t\tif(!isset($_POST['points']) || $_POST['points'] === ''){\n"
					"\t\t\t$ok = false;\n"
				"\t\t} else {\n"
					"\t\t\t$points = $_POST['points'];\n"
				"\t\t}\n\n")
	for num in range(1, picks+1):
		site.write("\t\tif(!isset($_POST['pick{}']) "
			"|| $_POST['pick{}'] === ''){}\n".format(num, num, '{'))
		site.write("\t\t\t$ok = false;\n")
		site.write("\t\t} else {\n")
		site.write("\t\t\t$pick{} = $_POST['pick{}'];\n".format(num, num))
		site.write("\t\t}\n\n")

	site.write("\t\tif(!$ok){\n")
	str1 = '\t\t\techo "'
	str1 += "<p style='color:red;'>"
	str1 += "Please make all picks!</p>"
	str1 += '";\n'
	site.write(str1)
	site.write("\t\t}\n")

	site.write("\t\tif($ok){\n"
			   "\t\t\t$nflpicks = fopen("
			   "'nflpicks.csv', 'a');\n")
	nflstr = '\t\t\tfwrite($nflpicks,'
	nflstr += r'"\n$name,'
	for num2 in range(1, picks+1):
		nflstr += '$pick{},'.format(num2)
	nflstr += "$points"
	nflstr += '");'
	site.write(nflstr+"\n")
	site.write("\t\t\t$name = '';\n")
	site.write("\t\t\t$points = '';\n")
	for num1 in range(1, picks+1):
		site.write("\t\t\t$pick{} = '';\n".format(num1))
	str1 = '\t\t\techo "'
	str1 += "<p style='color:green;'>"
	str1 += "Picks Submited</p>"
	str1 += '";\n'
	site.write(str1)
	site.write("\t\t}\n")
	site.write("\t}\n?>\n")

def form(site):
	site.write("<form method='post' action=''>\n")
	site.write("Name: <input type='text' name='name' value='<?php\n"
				"\techo htmlspecialchars($name);\n"
				"?>'><br>\n")
	with open('config.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['FAV', 'SPREAD', 'UNDER'])
		pickNum = 1
		for row in reader:
			num = str(pickNum)
			if(pickNum % 2 == 0):
				str1 = ("\n<span_2><input type='radio' name='pick{}' "
					"value='{}'\n".format(num, row['FAV']))
				str1 += "<?php\n\tif ($pick{} === '{}')".format(num, row['FAV'])
				str1 += "{\n\t\techo ' checked';\n\t}\n?>>\n"
				site.write(str1)
				site.write("<span style='padding-right:20px;'>"
					"{}</span>\n".format(row['FAV']))
				site.write("<span style='padding-right:10px;'>"
					"{}</span>\n".format(row['SPREAD']))
				site.write("<span style='text-align: right'>"
					"{}</span>\n".format(row['UNDER']))

				str1 = ("\n<input type='radio' name='pick{}' "
						"value='{}'\n".format(num, row['UNDER']))
				str1 += "<?php\n\tif ($pick{} === '{}')".format(num, row['UNDER'])
				str1 += "{\n\t\techo ' checked';\n\t}\n?>></span_2><br>\n"
				site.write(str1)
			else:
				str1 = ("\n<input type='radio' name='pick{}' "
						"value='{}'\n".format(num, row['FAV']))
				str1 += "<?php\n\tif ($pick{} === '{}')".format(num, row['FAV'])
				str1 += "{\n\t\techo ' checked';\n\t}\n?>>\n"
				site.write(str1)
				site.write("<span style='padding-right:20px;'>"
					"{}</span>\n".format(row['FAV']))
				site.write("<span style='padding-right:10px;'>"
					"{}</span>\n".format(row['SPREAD']))
				site.write("<span style='text-align: right'>"
					"{}</span>\n".format(row['UNDER']))

				str1 = ("\n<input type='radio' name='pick{}' "
						"value='{}'\n".format(num, row['UNDER']))
				str1 += "<?php\n\tif ($pick{} === '{}')".format(num, row['UNDER'])
				str1 += "{\n\t\techo ' checked';\n\t}\n?>><br>\n"
				site.write(str1)
			pickNum += 1
	csvfile.close()
	site.write("Points: <input type='text' name='points' value='<?php\n"
				"\techo htmlspecialchars($points);\n"
				"?>'><br>")
	site.write("<input type='submit' name='submit' value='Submit'>\n")

def gen_nflpick():
	nflpicks = open("/var/www/html/nflpicks.csv", 'w')
	with open('config.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['FAV', 'SPREAD', 'UNDER'])
		pickNum = 1
		nflpicks.write(",")
		for row in reader:
			nflpicks.write('"{}\n{}\n{}",'.format(row['FAV'],
												row['SPREAD'],
												row['UNDER']))
		nflpicks.write('"TIE\n-\nBRK"')
	nflpicks.close()

def main():
	site = open("/var/www/html/picks.php", "w")
	first_part(site)
	form_check(site)
	form(site)
	site.write("</form>\n"
			   "</body>\n"
			   "</html>")
	gen_nflpick()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="build website for picks")
    parser.add_argument("-u","--url",help="url of spreads",type=str)
    parser.add_argument("-g","--games",help="number of games this week",type=int)
    args = parser.parse_args()
    scrapper.build_config(args.url,args.games)	
    main()
