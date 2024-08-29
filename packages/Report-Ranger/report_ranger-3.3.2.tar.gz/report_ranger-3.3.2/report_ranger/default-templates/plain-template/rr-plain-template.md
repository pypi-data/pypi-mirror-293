---
defaults:
  company: ReporterSec
  appendixdir: 'appendices'
  hide_appendices: false
  hide_vulnerabilities: false
  output_file: "{{filename}}"
colors:
  white: ffffff
  rrsample: 6e7ad0
  open: 'E47676'
  closed: 'A9DA74'
  low: 'D3EAF9'
  medium: 'FFFF00'
  high: 'FF0000'
table_styles:
  heading:
    alias: 'h'
    bgcolor: rrsample
    bold: true
    color: white
latex:
  template: rr-latex-template.tex
csv:
  columns:
    '#': ref
    'Scope': scope
    'Name': name
    'Likelihood': likelihood
    'Impact': impact
    'Risk': risk
    'Risk Assessment': 'Risk assessment {-}'
    'Description': 'Description {-}'
    'Recommendations': 'Recommendations {-}'
riskassessment:
  name: Volkis Risk Assessment
  id: volkis
  stages:
    - name: Likelihood
      id: likelihood
      ratings:
      - Rare
      - Unlikely
      - Possible
      - Likely
    - name: Impact
      id: impact
      ratings:
      - Low
      - Moderate
      - Severe
      - Critical
  risks:
  - Low
  - Medium
  - High
  - Critical
  style_text:
    Low: 'low'
    Medium: 'medium'
    High: 'high'
    Critical: 'critical'
    Open: 'open'
    Closed: 'closed'
  colors:
    low: 'D3EAF9'
    medium: 'FFFF00'
    high: 'FF0000'
    critical: '7030A0'
    white: 'FFFFFF'
    open: 'E47676'
    closed: 'A9DA74'
  table_styles:
    critical:
      alias: 'C'
      color: 'white'
      bgcolor: 'critical'
      bold: true
      uppercase: true
      alignment: c
    high:
      alias: 'H'
      color: 'white'
      bgcolor: 'high'
      bold: true
      uppercase: true
      alignment: c
    medium:
      alias: 'M'
      bgcolor: 'medium'
      bold: true
      alignment: c
    low:
      alias: 'L'
      bgcolor: 'low'
      bold: true
      alignment: c
    open:
      alias: 'O'
      bgcolor: 'open'
      bold: true
      alignment: c
    closed:
      alias: 'C'
      bgcolor: 'closed'
      bold: true
      alignment: c
  matrix:
    Likely:
      Critical: Critical
      Low: Medium
      Moderate: High
      Severe: High
    Possible:
      Critical: Critical
      Low: Low
      Moderate: Medium
      Severe: High
    Rare:
      Critical: Medium
      Low: Low
      Moderate: Low
      Severe: Low
    Unlikely:
      Critical: High
      Low: Low
      Moderate: Medium
      Severe: Medium
  methodology: '
    A qualitative risk assessment is performed on each vulnerability to determine the impact and likelihood of the vulnerability being exploited. An overall risk is calculated based on the table below:

    {{
      table(ra.riskmatrixtable, headings="top-left", style_text=ra_style_text, colwidths=[18,10,10,10,10], colalign=["l","c","c","c","c"])
    }}
    
    The risk assessment methodology is derived from industry standards such as ISO
    31000[^1] and OWASP Risk Rating Methodology[^2].


    [^1]: https://www.iso.org/iso-31000-risk-management.html


    [^2]: https://www.owasp.org/index.php/OWASP_Risk_Rating_Methodology


    The impact rating is deduced from multiple factors that consider both technical
    impact and business impact:


    * **Loss of confidentiality**: How much sensitive information could be accessed
    or leaked and how sensitive was it?

    * **Loss of integrity**: How much data could be corrupted and what degree of corruption
    was possible? Was it possible to perform actions on behalf of others?

    * **Loss of availability**: How much services could be disrupted, preventing users
    from performing their tasks? What was the degree of impairment?

    * **Financial damage**: How much money could be lost as a result?

    * **Reputational damage**: How badly would the company''s reputation be damaged
    and how much trust could customers lose?

    * **Non-compliance**: Would the business be in breach of certain compliance standards
    they are obliged to comply with? (E.g. Privacy Act)


    The likelihood is deduced from considering who the adversary may be and factors
    around the vulnerability:


    * **Skill of adversary**: How skilful is the attacker likely to be?

    * **Motive**: What are the motivating factors that the adversary may have?

    * **Resources**: How much time and economic resources does the adversary have?

    * **Ease of discovery**: How likely is the adversary to discover the vulnerability?

    * **Ease of exploitation**: How easy is the vulnerability to exploit and are there
    publicly available tools to aid in doing so?

    * **Detection**: How likely is the attack to be discovered by the organisation?


    An overall rating (from Low to Critical) is given to each vulnerability. The vulnerabilities
    are then sorted in order from importance and urgency to remediate.


    '
---

{{reportbody}}
