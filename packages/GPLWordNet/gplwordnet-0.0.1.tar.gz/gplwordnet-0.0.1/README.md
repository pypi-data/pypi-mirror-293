
## Introduction
GPLWordNey is a lexcion generating tool, using WordNet as database to find two sets of lexcions.

It provides:
- full expand - This function is used for finding target words' antonyms, synsets, adjectives, derivational words, and hyponyms.
- antonyms expand - This function is used for finding target words' antonyms

Testing:

Test can then be run after installation with:
```{python}
    data1 = [{'term': 'good', 'PoS': 'ADJECTIVE'}]
    print(full_expand(data1))
    
    data2 = [{'term': 'good', 'PoS': 'ADJECTIVE'},
          {'term': 'competence', 'PoS': 'Noun'}]
    print(full_expand(data2))
    
    data3 = [{'term': 'good', 'PoS': 'ADV', 'sense': 1},
          {'term': 'competence', 'PoS': 'Noun'}]
    print(antonyms_expand(data3))
```
## Supplemantal Materials
1. This work is an replication work of Nicolas' SADCAT codes, which only have R version. For more details about Nicolas Works, please refer to following link,
   - [Nicolas dictonaries Webpage](https://gandalfnicolas.github.io/SADCAT/)
   - [Nicolas GitHub](https://github.com/gandalfnicolas/SADCAT)

2. The approach I mainly learned from Maks et al.'s(2014) Paper.
   - [Generating Polarity Lexicons with WordNet propagation in five languages](http://www.lrec-conf.org/proceedings/lrec2014/pdf/847_Paper.pdf)

## Call for Contributions
The GPLWordNet project welcomes your expertise and enthusiasm!

Small improvments of fixes are always appreciated, please submit your feature according GitHUb.

Our preferred channels of communication are all public, but if you’d like to speak to us in private first, contact my public email at xuanlongqin.cu@gmail.com . 




