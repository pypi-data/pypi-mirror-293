from ecl_api import ECL, ECLEntry
import xml.etree.ElementTree as ET

print('Input password:')
password = input()

ecl = ECL(url='https://dbweb9.fnal.gov:8443/ECL/sbnd/E', user='sbndprm', password=password)

text = ecl.search(category='Shift', limit=3)
# print('->', len(text_))
# print(text)
# print('Entry date:', text.split('timestamp="')[1].split('"')[0])

xml = ET.fromstring(text)
entries = xml.findall('./entry')

# for entry in entries:
    # print('---')
    # print(entry.attrib['form'])
    # print(entry.attrib)
    # print(entry.tag)
    # for child in entry:
    #     print(child.tag, child.attrib)


    # print(ET.tostring(entry))
    # break
    # text = entry.find('./text').text
    # print(text)

    # if 'Purity Monitors Automated Plots' in text:

    #     timestr = entry.attrib['timestamp']
    #     lasttime = datetime.datetime.strptime(timestr, "%m/%d/%Y %H:%M:%S")
    #     break



ecl.get_entry(entry_id=7252)


# text=f'<font face="arial"> <b>Purity Monitors Automated Plots</b> <BR> TEST </font>'

entry = ECLEntry(category='Shift', formname='Shift run start checklist - v1')

form = {
    "Maximize the window": "Yes",
    "Date": "07/23/24",
    "Time": "19:39:58",
    "Run number": "00000",
    "DAQ Components": "testentry",
    "Configuration": "testentry" 
}

entry.set_form_elements(form)

# for name, filename in self._current_plots.items():
#     entry.add_image(name=name, filename=filename)

print(entry.show(pretty=True))


