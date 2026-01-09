#!/usr/bin/env bash
# Bash completion for xnLinkFinder

_xnlinkfinder_completions() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main options
    opts="-i --input -o --output -op --output-params -owl --output-wordlist"
    opts="$opts -oo --output-oos -ow --output-overwrite -sp --scope-prefix"
    opts="$opts -spo --scope-prefix-only -sf --scope-filter -c --cookies"
    opts="$opts -H --headers -r --regex -ra --regex-after -d --depth"
    opts="$opts -p --processes -x --exclude -orig --origin -t --timeout"
    opts="$opts -inc --include -u --user-agent -insecure -s429 -s403"
    opts="$opts -replay-proxy --config -nb --no-banner -v --verbose"
    opts="$opts -vv --vverbose --version --stream --preset"
    opts="$opts --auto-scope --parse-robots --parse-sitemap"
    opts="$opts --spider --spider-depth --generate-sitemap"
    opts="$opts --graph --graph-format --generate-nuclei --nuclei-output"
    opts="$opts --lang --metrics --dashboard"
    
    # Option-specific completions
    case "${prev}" in
        -i|--input)
            COMPREPLY=( $(compgen -f "${cur}") )
            return 0
            ;;
        -o|--output|-op|--output-params|-owl|--output-wordlist|-oo|--output-oos)
            COMPREPLY=( $(compgen -f "${cur}") )
            return 0
            ;;
        --preset)
            COMPREPLY=( $(compgen -W "bug_bounty pentest recon stealth aggressive api_hunting js_analysis" -- "${cur}") )
            return 0
            ;;
        --graph-format)
            COMPREPLY=( $(compgen -W "html dot gexf graphml json" -- "${cur}") )
            return 0
            ;;
        --lang)
            COMPREPLY=( $(compgen -W "en es fr de zh ar ja ru" -- "${cur}") )
            return 0
            ;;
        -d|--depth|--spider-depth)
            COMPREPLY=( $(compgen -W "1 2 3 4 5 10" -- "${cur}") )
            return 0
            ;;
        -p|--processes)
            COMPREPLY=( $(compgen -W "1 2 5 10 20" -- "${cur}") )
            return 0
            ;;
        *)
            ;;
    esac
    
    COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
    return 0
}

complete -F _xnlinkfinder_completions xnLinkFinder
complete -F _xnlinkfinder_completions xnlinkfinder
