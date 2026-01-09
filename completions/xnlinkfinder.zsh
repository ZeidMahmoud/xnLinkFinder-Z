#compdef xnLinkFinder xnlinkfinder
# Zsh completion for xnLinkFinder

_xnlinkfinder() {
    local -a options
    options=(
        '-i[Input URL or file]:file:_files'
        '--input[Input URL or file]:file:_files'
        '-o[Output file]:file:_files'
        '--output[Output file]:file:_files'
        '-op[Output parameters file]:file:_files'
        '--output-params[Output parameters file]:file:_files'
        '-owl[Output wordlist file]:file:_files'
        '--output-wordlist[Output wordlist file]:file:_files'
        '--preset[Use preset configuration]:preset:(bug_bounty pentest recon stealth aggressive api_hunting js_analysis)'
        '--graph[Generate link relationship graph]'
        '--graph-format[Graph output format]:format:(html dot gexf graphml json)'
        '--generate-nuclei[Generate nuclei templates]'
        '--nuclei-output[Nuclei templates output directory]:directory:_directories'
        '--stream[Stream output in real-time]'
        '--auto-scope[Auto-detect scope]'
        '--parse-robots[Parse robots.txt]'
        '--parse-sitemap[Parse sitemap.xml]'
        '--spider[Enable spider mode]'
        '--spider-depth[Spider depth]:depth:(1 2 3 4 5 10)'
        '--generate-sitemap[Generate sitemap.xml]'
        '--lang[Set output language]:language:(en es fr de zh ar ja ru)'
        '--metrics[Enable metrics collection]'
        '--dashboard[Launch web dashboard]'
        '-d[Crawl depth]:depth:(1 2 3 4 5 10)'
        '--depth[Crawl depth]:depth:(1 2 3 4 5 10)'
        '-p[Number of processes]:processes:(1 2 5 10 20)'
        '--processes[Number of processes]:processes:(1 2 5 10 20)'
        '-v[Verbose output]'
        '--verbose[Verbose output]'
        '-vv[Very verbose output]'
        '--vverbose[Very verbose output]'
        '--version[Show version]'
        '-nb[No banner]'
        '--no-banner[No banner]'
    )
    
    _arguments -s $options
}

_xnlinkfinder "$@"
