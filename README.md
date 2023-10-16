# Text-Mapper

Allows simple newline seperated data to be mapped on to more complex text files. Specificially designed to work with .html files, it allows webpage elements that are repeated to be created only once, and then duplicated for every instance of data. 
This means that a change to an element with multiple instances is automatically replicated on other instances. Additionally, it allows an individual who is uncomfortable working with HTML directly to alter the text on a web page with out
fear of damaging the structure of the page.

It can be run directly, which will prompt the user for file paths, or it can be run with a file as an argument, in which case it will assume it has the format "myFile.fmt.html" and will look for data in "myFile.txt" and output the result as "myFile.html".

The syntax for the files is as follows:
- Format file:
  - {} denotes that one line of text is to be placed in a location
  - #SECSTART denotes the start of a repeating section (nesting is acceptable)
  - #SECEND denotes the end of a repeating section
- Data files:
  - Each line is a string which will replace on instance of {} in the format file
  - ~ denotes the end of a section's data
  - List lengths that do no align with the format file will leave unreplaced {}
