# Task

Analyse the following job description for job matching.

# Extract skills

Extract the most relevant skills for this specific vacancy.

Include:
- programming languages
- frameworks
- libraries
- cloud technologies
- databases
- automation tools
- software and platforms
- other concrete technical or professional hard skills

Rules:
- Only include skills explicitly stated or clearly supported by the job description.
- A technology appearing anywhere in the description is not sufficient by itself.
- A skill should be directly connected to the responsibilities or requirements of this specific role.
- Do not include soft skills, personality traits, benefits, generic phrases, or general responsibilities.
- Do not include unrelated technologies mentioned elsewhere in the description.
- Do not include broad company-wide technology catalogues when those technologies are not relevant to this particular role.
- Do not infer skills that are not supported by the description.
- Return at most 10 skills.
- Prioritise the most important skills for matching a candidate to this vacancy.

# Determine role

Identify the primary job category represented by the specific vacancy.

Use the following signals, in order of importance:
1. Advertised job title
2. Primary responsibilities
3. Required qualifications and experience

Keep the role semantically equivalent to the advertised occupation.

For example, do not replace a role such as "Labourer" with a technical engineering role merely because the description mentions engineering or technical activities.

If the listing is a general talent pool, speculative application, "future opportunities" listing, or does not describe a concrete vacancy, return "unknown".

# Determine seniority

Infer seniority from:
- years of experience
- senior/junior wording
- responsibilities
- leadership expectations

If seniority cannot be determined confidently, return "unknown".

# Inputs

Job Description:

{{job_description}}

# Output

Return only JSON.