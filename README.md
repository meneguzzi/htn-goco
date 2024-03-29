# HTN-GoCo

[![DOI](https://zenodo.org/badge/48817866.svg)](https://zenodo.org/badge/latestdoi/48817866)

Repository for the code used in the goals and commitments planning framework developed by Meneguzzi, Telang and others. 
The following papers discuss this in more theoretical detail:

- MENEGUZZI, F.; MAGNAGUAGNO, M. C.; SINGH, Munindar; TELANG, Pankaj; and YORKE-SMITH, Neil. [GoCo: Planning Expressive Commitment Protocols. Autonomous Agents and Multi-agent Systems](https://doi.org/10.1007/s10458-018-9385-0), vol 32:4, pp 459–502, 2018. 
- MENEGUZZI, Felipe; TELANG, Pankaj and SINGH, Munindar P. [A First-Order Formalization of Commitments and Goals](http://www.aaai.org/ocs/index.php/AAAI/AAAI13/paper/view/6371/7241), In Proceedings of the 27th AAAI Conference on Artificial Intelligence (AAAI), Bellevue, WA, USA, 2013. 
- TELANG, Pankaj; MENEGUZZI, Felipe and SINGH, Munindar P. [Hierarchical Planning about Goals and Commitments](http://www.csc.ncsu.edu/faculty/mpsingh/papers/mas/AAMAS-13-HTN.pdf), In Proceedings of the 12th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), Saint Paul, MN, USA, 2013. 
- MENEGUZZI, Felipe; TELANG, Pankaj R. and YORKE-SMITH, Neil. [Towards Planning Uncertain Commitment Protocols](http://www.aamas2015.com/en/AAMAS_2015_USB/aamas/p1681.pdf), In Proceedings of the 14th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), Istanbul, Turkey, 2015. 

If you use this software in your research, please consider citing the papers above.

## Running Instructions
First ensure that JSHOP is in the CLASSPATH (both antlr.jar and JSHOP2.jar must be in the CLASSPATH)
Then run compile.sh using as parameters the name of the domain (without .jshop) and the name of the problem (also without .shop), with either run or gui as the third parameter.
For example, to compile and run a domain stored in cg.jshop with a problem stored in pb1.jshop, the command would be:

```bash
./compile.sh gb pb1 run
```

## Installing JSHOP2
[JSHOP2](https://sourceforge.net/projects/shop/files/JSHOP2/) lives in Sourceforge, but it seems to have been abandoned. If you really like Github, some people mirrored it at [https://github.com/mas-group/jshop2](https://github.com/mas-group/jshop2)
