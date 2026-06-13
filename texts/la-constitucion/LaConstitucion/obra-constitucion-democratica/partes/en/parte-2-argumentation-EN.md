
# THE DEMOCRATIC CONSTITUTION

**Part 2: Argumentation and Philosophy**

**The why behind every design decision**

---

# INTRODUCTION: DESIGN PHILOSOPHY

## The problem this Constitution solves

Most current "democracies" are elective oligarchies disguised as democracies. The appearance exists: periodic elections, parliament, a separation of functions that pretends to be a separation of powers. The substance does not: parties strongly or completely control candidate selection, financing, and media. The result is an illusion of choice managed by elites. An honest aristocracy is preferable to a false democracy.

Current constitutions are many and diverse: each country has its own, with its own principles, history, and compromises. Attempting to reform them one by one would be a titanic and endless effort. But power dynamics do not understand specific cultures. The tendency to concentrate power, to corrupt institutions, to capture control mechanisms: these are human constants, not cultural ones. If the problem is universal, the solution can be too. This Constitution seeks to be that solution: a reference framework agnostic to any historical or cultural context, based solely on how power works among human beings.

This Constitution does not assume good will. It assumes the worst case: an actor with unlimited resources attempting to capture the system. Every mechanism is designed so that this worst case is as expensive, difficult, and risky as possible. It is a security audit of democracy, not a manifesto of hope.

## Defensive mindset

The design follows the mindset of a security hacker: not asking "will it work if everyone cooperates?" but "how will it break, and how would it self-repair if someone attacks?" Every mechanism is subjected to the question: what is the attack vector? How much does it cost to exploit? How is the abuse or attack detected?

## Corruption cost framework

Central principle: every system has a price. The design must maximize that price. There is no moralizing about whether people become corrupt or not; it is assumed they can be bought, and the design ensures that the cost of buying them is as high as possible within the natural and social limits of human beings. This is quantified through the 25th percentile of income (P25) as an economic proxy of the cost of influence; the rationale for this decision is explained further on.

## Democratic trilemma

Analogous to the blockchain trilemma (decentralization, security, scalability), democracy faces: Democracy <-> Efficiency <-> Stability. All three cannot be maximized. This Constitution chooses:

1. Maximize democracy (popular control is the ultimate source of legitimacy).
2. Then efficiency (representatives manage day-to-day affairs).
3. Then stability (speed can be sacrificed for robustness).

## Conscious theoretical influences

- Antonio Garcia Trevijano: single-member districts, runoff elections, revocability, mutual assured destruction, no party financing. This Constitution largely adopts his framework and adds specific details to complete it.

- Robert Michels: Iron Law of Oligarchy. Every organization tends to concentrate power. The design works against this.

- Decentralized systems design: the author is a software engineer and blockchain hacker. The design mindset of this Constitution derives largely from the engineering of distributed systems resistant to attacks: Byzantine fault tolerance (the system works even if some nodes are malicious), elimination of single points of failure (no single body concentrates all power), consensus mechanisms with variable thresholds (levels N1-N6), public auditability and verifiability (budgetary transparency, verifiable voting), and probabilistic immutability of fundamental rules. Additionally, certain ideas from operating systems such as a bootstrap process also stem from this influence.

- Cheerfulism: the author's own philosophy. Its central thesis is that happiness -- not freedom -- is the deepest driver of human behavior, and that abuse has six natural sources (ignorance, selfishness, laziness, and their counterparts of capacity). The corruption cost framework, the argument of the ever-increasing complexity of human wisdom, and the conclusion that democracy is the natural destination of power dynamics all originate from this work.

Any coincidence between the principles of this Constitution and those of other thinkers, philosophers, or political theorists not mentioned here is exactly that: coincidence. My apologies if I have not named them; I am simply not aware of them.

The design starts from first principles (how power works, how a system is attacked, how much it costs to corrupt it) and not from extensive reading of pre-existing theoretical frameworks.

That the conclusions converge with those of other thinkers neither invalidates nor validates the design; it simply suggests that the fundamental problems of power tend to produce similar solutions when analyzed with rigor.

---
---

# WHAT IS DEMOCRACY AND WHY A DEMOCRACY

Before explaining each design decision of this Constitution, it is worth establishing a shared starting point between reader and writer: what we understand by democracy, why we should bet on it, and what its real limits are.

## Definition

The word democracy comes from the Greek: demos (people) and kratos (power). Power of the people. But this etymology is insufficient as an operational definition. "Power resides in the people" is a nice declaration that says nothing about how the system actually works.

An operational definition of democracy requires three elements:

**1. Open competition for power.** Any group of citizens, by the mere fact of being citizens, can organize to aspire to manage the State. No approval from existing groups is needed, nor must they follow predetermined internal structures. The only requirement is being citizens. This is analogous to perfect competition in economics: anyone who can manufacture a better product can access the means to create it. In democracy, anyone who has a vision for their society can create a group to reflect it and present it to their neighbors.

**2. Real separation of powers.** The State has three natural functions: to legislate (create the rules), to execute (apply them), and to judge (resolve conflicts when the rules are broken). In a democracy, these three functions are exercised by bodies independent of each other, with independence of appointment and financing. Without this separation, democracy collapses into oligarchy: a group that simultaneously legislates, executes, and judges has no limit to what it can do. It may collapse into a plutocratic oligarchy, or a technocratic one, or both at once; regardless of the system, it collapses into oligarchy, or even dictatorship.

**3. Real representation with accountability.** In large societies, direct democracy is unfeasible for daily management. Representatives are needed. But representation is only democratic if it meets two conditions: the representative is directly elected by a community small enough to know them (single-member districts), and that community can dismiss them at any time if they fail to deliver (revocability). Without these two conditions, the representative serves the party that placed them on the list, not the citizen who voted for them. For power would be transferred and not delegated, thus extracting the kratos (power) from the demos (people).

In more technical terms: democracy is a coordination protocol for power dynamics whose result is the most optimal possible partition of powers within the State. That is, the protocol that minimizes the centralization of power in any individual actor or groups and maximizes the dynamism of the functioning of the power structure.

## Arguments for and against democracy

### In favor

#### Democracy produces the richest feedback loop

All human progress is based on feedback loops: act, observe the result, correct, act again. We learn this way. Science works this way. Evolution works this way.

In a dictatorship, the feedback loop is poor: one person decides, and information about whether that decision was good or bad arrives filtered, late, and distorted by fear. In an oligarchy, the loop is somewhat richer but remains limited to the group in power. In a democracy, the loop includes the entire society: millions of people evaluating decisions, proposing alternatives, correcting errors. The more diverse perspectives participate in the loop, the better reality is understood and the better it can be responded to.

#### Democracy reflects human biology

The human brain cannot process all the information it receives. Its solution is to fix some variables (beliefs, habits, certainties) while varying others (exploration, trial and error). The fixed variables provide stability; the free variables provide adaptability.

Every power system replicates this mechanism at the social scale: laws are the fixed variables (stability and predictability) and the mechanisms of political change are the free variables (adaptation). This is true in dictatorships, oligarchies, and democracies alike. The difference is the richness with which each system allows the dynamic part to be exercised.

In a dictatorship, one person changes the variables. In an oligarchy, a small group. In a democracy, periodic elections allow the entire society to participate in deciding which fixed variables no longer work and must change, and revocability adds an emergency mechanism when change cannot wait for the next cycle. By the same feedback loop argument: the more diverse perspectives participate in the process of fixing and unfixing variables, the richer the result. Democracy is the system that best connects the static stability our nature needs with the dynamism that enables adaptation.

#### Decentralization minimizes abuse

All power, given enough time, tends toward abuse. This is not cynicism: it is a constant empirical observation throughout human history and in computer cybersecurity systems, designed and operated by humans. The question is not "will they abuse?" but "how much damage can they do when they abuse, and how can we minimize the damage done and repair it as much as possible if they manage to abuse?"

The answer depends on how much power each individual concentrates. In a dictatorship, a single individual concentrates everything: the potential damage is maximum. In a democracy, power is distributed among many independent actors: district legislators, a separate executive, an independent judiciary, and a people with the capacity for direct intervention. The damage any individual actor or group can do is limited by the others. Abuse is not eliminated -- abuse is a natural human phenomenon; its scope and impact are systematically minimized.

#### The ever-increasing complexity makes democracy inevitable

This is the argument of the ever-increasing complexity of human wisdom. Each generation inherits the accumulated knowledge of its predecessors and adds its own. The complexity of human societies never stops growing: more technology, more interconnection, more variables to manage. A centralized protocol that worked for a village of 500 people does not work for a city of 5 million. A protocol that worked in the 18th century does not work in the 21st.

Centralized and static systems have a ceiling of complexity they can manage. When society exceeds that ceiling, the system fractures: in the form of violence, silent misery, or unsustainable social pressure. Democracy, by distributing decision-making and allowing periodic renewal, has a higher complexity ceiling. It is not infinite, but it is significantly higher.

Put another way: although more centralized systems may be the temporary solution that works now and worked in the past, sooner or later they stop working. The increasing complexity of human knowledge is a curse (or a blessing) that inevitably pushes toward more decentralized and dynamic protocols capable of handling all variables in a more adaptive way.

#### The separation of powers prevents the natural drift toward tyranny

Without separation of powers, a democratically elected group that controls the entire State will end up, by natural tendency, modifying the rules to stay in power. Not necessarily out of malice, but out of incentives: whoever has the power to change the rules and the incentive to retain power will end up changing the rules in their favor. The separation of powers breaks this cycle: whoever makes the laws neither executes them nor interprets them, whoever executes them neither judges whether they are followed nor creates them, and whoever judges neither writes them nor enforces them.

#### Democracy enables specialization

In a centralized system, the ruler must simultaneously be an expert in economics, defense, healthcare, education, infrastructure, and diplomacy. Nobody is. In a democracy, the separation of functions allows specialists to emerge in regional management (district representatives) alongside technical specialists (ministries, agencies, private companies and organizations). Each can do their job well because they do not have to do everything. It is the principle of separation of responsibilities improving the production of a product applied to governance.

### Against

#### Giving a gun to a monkey

The strongest argument against democracy is also the most uncomfortable: decentralization and dynamism only work well if they are granted to individuals with sufficient capacity to manage them. Giving decision-making power over complex systems to people who do not understand those systems produces bad decisions. In blunt terms, it is like giving a gun to a monkey.

This is not an elitist argument: it is an observation about the relationship between complexity and cognitive capacity. A voter who does not understand how the tax system works cannot rationally evaluate tax proposals. A voter who does not understand geopolitics cannot accurately evaluate -- that is, in accordance with their interests -- foreign policy decisions. Democracy assumes that the aggregation of millions of partially informed decisions produces a reasonable result. Sometimes it does. Sometimes it does not.

#### Democracy is harder to design than any other system

Designing a functional democratic constitution is a task of extraordinary complexity. A dictatorship does not need to deeply worry about incentive design, power balances, unambiguous drafting, or self-correction mechanisms. A democracy does. A poorly designed democracy naturally collapses into oligarchy or dictatorship, because the actors with the most resources end up exploiting the weaknesses of the design.

The paradox is that the system requiring the most intelligence for its design is precisely the one that grants power to people who may not have that intelligence. A dictatorship is easy to design and hard to live under. A democracy is hard to design and, if well designed, less hard to live under.

#### The problem of simplified truths

As societies grow, no individual can know everything sufficiently well. People demand simple explanations for complex realities. Politicians know this and exploit the demand: they simplify, polarize, reduce multidimensional problems to one-sentence slogans. Citizens align with the simplification that most comforts them, not with the one that best describes reality or best solves a problem. This generates a vicious cycle: the more politicians simplify, the more society polarizes, the wider the gap between rulers and ruled, and the worse democracy functions.

This problem is not exclusive to democracy: it is a problem of all high-complexity human societies, regardless of their power system. But what is relevant here is that democracy does not solve it either. Democracy is not a marvel that solves everything; it is the best available protocol, with real limitations that should be recognized without disguising them.

#### The oligarchic tendency is inherent to humans

Even within democratic systems, organizations tend to concentrate power in few hands. This is the Iron Law of Oligarchy by Michels: every party, union, or movement ends up dominated by an internal elite. In practice, even the best-designed democracies tend toward alternation between two or a few dominant parties. Constitutional mechanisms can limit this tendency but not eliminate it.

Graph theory offers a structural explanation for why. If a society is modeled as a graph where each person is a node and each relationship is an edge, the number of possible relationships grows combinatorially. The simplest case: with 3 people (A, B, and C) there are exactly 3 possible relationships: A with B, B with C, and C with A. It seems manageable. But with 10 people there are 45 relationships. With 100, there are 4,950. With 1,000, there are nearly 500,000. And the possible alliances (subgroups of 2 or more people that can form) grow even faster. No human brain can process that many relationships simultaneously. The result is that, as a group grows, its members need to simplify: delegate, concentrate decisions, create hierarchies. Not out of malice or design flaw, but because the combinatorial complexity exceeds the cognitive limits of the individual. The oligarchic tendency is not a flaw of democracy; it is a consequence of the biological limits of the human brain operating in large groups.

#### No political system resolves problems between States

Democracy works within a State because there is a shared legal framework, a monopoly on violence, and a judicial system that arbitrates conflicts. Between States, none of this exists. There is no world judge, no international law with teeth, no police to enforce it. Internal democracy does not protect against external aggression from a more powerful State that does not respect agreements. Democratic mechanisms have a perimeter: the borders of the State.

Again, this is not a problem exclusive to democracy: no political system -- dictatorship, oligarchy, or democracy -- solves by itself the relations between sovereign States. But it is worth mentioning so as not to attribute to democracy capabilities it does not have.

### Conclusion: democracy as a destination

The arguments against are real. Giving a gun to a monkey is a real risk. The difficulty of design is real. The oligarchic tendency is inherent to the cognitive limits of the human brain operating in large groups. Simplified truths and polarization are problems of every complex society that democracy does not solve. And no political system, democratic or otherwise, solves by itself the relations between sovereign States. Democracy is not a perfect system nor does it guarantee good results.

But the arguments in favor are structural. The argument of the ever-increasing complexity of human wisdom inevitably pushes toward more decentralized and dynamic systems. It is not a matter of ideological preference: it is a consequence of how the human species accumulates knowledge. As long as we continue reproducing, preserving, and transmitting knowledge, our societies will do nothing but increase in complexity. And there will be a point -- different for each society -- at which the more centralized and static protocols simply will not be sufficient. Democracy produces the richest feedback loop, better reflects human biology by connecting stability with adaptation, systematically minimizes the scope of abuse, and enables specialization in the management of the State.

Democracy is not the perfect system. But it is the protocol of power dynamics with the highest complexity ceiling among those involving a State. It is the one that best scales with the increasing complexity of human societies.

Its main weakness -- giving a gun to a monkey -- is not solved with less democracy, but with more education. The solution to the monkey with the gun is not to take away the gun; it is to teach it how to use it. This Constitution cannot solve that problem (education is a legislative and personal competence, not a constitutional one), but it can create the framework in which the solution is possible.

Democracy is, ultimately, a destination: not because it is inevitable at every moment and place, but because the natural direction of human complexity in prosperous societies points toward it and ends up requiring it. Societies that do not reach it will suffer more pressure, more friction, and more violence than those that do. It is not a promise of paradise. It is the realization that, among all available power protocols, this is the one that functions least badly in the long run.

With this definition, these arguments, and these limitations in mind, it is time to get into the details. What follows is the explanation of how each article of this Constitution reflects the dynamics described, and why each design decision is the way it is.

---
---
---
---

# TITLE I: FUNDAMENTAL PRINCIPLES

## Article 1: Popular Sovereignty and Hierarchy of Legitimacy

Sovereignty resides in the people not as a rhetorical declaration, but as an operative principle. The hierarchy of legitimacy establishes two levels: Popular Power above the three delegated powers (Legislative, Executive, and Judicial), which are equal among themselves. It is not a blank check: it is a principle of precedence with rules.

Why are the three powers equal? Because real separation of powers requires that no power prevails over another. If the Legislative could directly nullify judicial decisions, judicial independence crumbles. If the Judiciary could legislate, popular representation loses its meaning. The relationship between the three powers is not hierarchical but one of mutual control: the Judiciary reviews the constitutionality of laws (Article 43) and legislators are criminally liable if they legislate against the Constitution (Article 44). In both cases, being wrong has consequences. This bidirectional accountability replaces hierarchy: there is no need for one to be "above" the other when both pay for their mistakes.

Why only in the cases the Constitution explicitly describes? Here the democratic trilemma comes in: democracy, efficiency, and stability cannot be maximized simultaneously. If the people could nullify any decision of any power at any time, direct democracy would be maximized but the system would be chaotic and inoperable: no government could govern, no judge could judge, no law would have enough stability to be applied. The hierarchy of legitimacy operates only through specific constitutional mechanisms (popular nullification, revocation, elections) precisely to balance popular control with the State's operational capacity.

## Article 2: Consensus Levels

The six consensus levels are the operational tool of the entire Constitution. Each level represents a different degree of social agreement, from simple majority to near-unanimous consensus. In classical terminology: N1 (51%) is simple majority, N2 (60%) reinforced majority, N3 (66%) qualified majority, N4 (75%) supermajority, N5 (85%) reinforced supermajority, and N6 (95%) quasi-unanimity. The constitutional text uses exclusively the percentage as the formal definition, without descriptive labels, to avoid ambiguities such as the one that would exist between "two-thirds" (66.67%) and "66%." The idea is that more transcendental decisions require broader agreements: changing an ordinary law requires N1, but modifying an entrenched clause requires N6. The formal definition in its own article avoids ambiguities: every time the Constitution says "Level N3 consensus," the meaning is exact and does not depend on interpretation.

The parameters protected at N6 are those that define the fundamental structure of the electoral system and the mechanisms of direct democratic control: how one is elected, how one is recalled, and how one is removed. Modifying these parameters alters the balance of power between the people and their representatives, which is why they require quasi-unanimity. The parameters protected at N5 are structural but not electoral: judicial composition, requirements for access to judicial positions, constitutional cycles. The remaining parameters are governed by the ordinary reform procedure (N4, Article 68).

## Article 3: Constitutional Subjects

The Constitution needs precise vocabulary for its subjects, just as a program needs well-defined types. Without this definition, every article that says "citizen" is ambiguous: does it include a tourist? A minor? A resident without nationality? Terminological ambiguity is an interpretive attack vector: a creative court can expand or restrict the scope of a right depending on how it interprets "citizen."

The three categories (person, citizen, citizen with the right to vote) are inclusively cascading: every voter is a citizen, every citizen is a person, but not the reverse. This allows rights such as personal integrity to apply to every person (including tourists, refugees, residents without nationality), while political capacities such as voting or initiating revocations are reserved for citizens with the right to vote.

The approach is "everything by default, explicit exceptions": each category enjoys all the rights of its level unless expressly restricted. This minimizes the necessary text and reduces the interpretive attack surface: if the Constitution does not explicitly state that a right is restricted for a category, it is not.

The clause on criminal convictions avoids creating a fourth category of subject ("criminal"). A convicted person does not lose their status as a person or citizen: they lose specific rights determined by law and the sentence, within constitutional limits. This is analogous to a permissions system in software: the user is not deleted, specific permissions are revoked.

A theoretical threat to keep in mind: nationality is defined "in accordance with the law," which means the Legislature could tighten nationality requirements to indirectly reduce the electorate without technically "restricting suffrage" (Article 4). This Constitution does not define who is a citizen -- it delegates this to law. This is a slow attack vector: each individual tightening seems reasonable, but cumulatively they exclude sectors of the population. Constitutionality review (Articles 42-43), equality before the law (Article 8), and the entrenched protection of universal suffrage (Article 66) make this path difficult, but do not eliminate it entirely. It is a conscious limitation: defining nationality in the Constitution would make it rigid in the face of changing demographic realities; delegating it to law makes it flexible but vulnerable. Flexibility with counterweights is chosen.

## Article 4: Universal Suffrage

Suffrage cannot be restricted. The justification is direct: by the same feedback loop argument, the more citizens participate in the democratic process, the more perspectives enter the system, the more information is processed, and the better the collective capacity to find optimal solutions. Restricting suffrage impoverishes the loop. Any exception (such as judicial declarations of incapacity) opens the door to arbitrary restriction of voting on political grounds: a corrupt judge could declare "incapable" thousands of voters in a key district. The risk of opening that door exceeds the benefit of closing it.

In general terms, opening the door to certain conditions that permit excluding voters is an extremely difficult door to monitor in a democracy. Human attention is a limited resource: citizens cannot pay attention to everything being legislated simultaneously. And in the current era, with internet and social media addiction, it is easier than ever to distract the population while legislating to gradually restrict who can vote and who cannot. It is a slow and silent attack vector: each individual restriction seems reasonable, but cumulatively they extract power from the demos (the people). It is preferable -- and I would say vital -- not to open that door at all. Or in any case, under Level N6 consensus conditions, which is precisely designed to ensure that any change of this kind is the result of a deep social consciousness and not a momentary outburst of anger or manipulation through social media or other means.

## Articles 5 and 17: Secrecy, Vote Verifiability, and Remote Voting

Three simultaneous properties: secrecy (nobody knows what you voted), verifiability (you can verify that your vote was counted), and public auditability (anyone can verify the process). These three properties are the minimum characteristics of any legitimate voting system, both in-person (Article 5) and remote (Article 17). The Constitution does not prescribe the technology (blockchain, cryptography, paper and ballot boxes) because what matters are the characteristics that the process must meet, not the method by which it meets them. If tomorrow a technology superior to blockchain combined with zero-knowledge cryptography emerges, it can be adopted without constitutional reform. What remains invariant are the required characteristics.

The legitimacy of the vote emerges from the absence of coercion in the process. If the vote is secret, nobody can pressure you to vote a specific way. If it is verifiable, nobody can falsify it without your detecting it. If it is auditable, nobody can manipulate the count without society discovering it. Under these conditions, each individual can look after their interests honestly, and it is this aggregated honesty that strengthens the feedback loop that enriches democratic solutions.

These guarantees would be empty without consequences for their violation. That is why Article 5 establishes an electoral nullity mechanism: if the votes affected by a violation of the guarantees are sufficient to have altered the result, the election is declared null and must be repeated. The threshold avoids two extremes: an attacker sacrificing pawns and preserving a fraudulent result (no nullity), or a saboteur compromising a few votes to force the repetition of an election they lost (automatic nullity without a threshold). Any citizen with the right to vote can initiate the procedure before the Judiciary.

## Article 6: Guarantee of Popular Nullification

This article guarantees that a mechanism for direct popular nullification can always exist. It does not impose one (the specific mechanism is defined during the Bootstrap or by subsequent legislation), but it prohibits any power of the State from blocking its creation. It is insurance against legislative capture: if parliament passes laws against the popular interest, the people always have the nuclear option of nullifying them directly, with the same consensus level that was needed to approve them.

The calculation base is deliberately asymmetric: a law approved with N1 of the Legislature (51% of seats) requires N1 of the citizen census (51% of all citizens with the right to vote) to be nullified. This asymmetry is inherent to the difference between representative and direct democracy. Popular nullification is not intended to be a routine mechanism but an emergency valve for deeply unpopular measures whose correction cannot wait for the district-by-district revocation cycle.

### Exception for state of emergency legislation

The general rule of Article 6 assumes a level playing field between State and people: the same consensus level to approve as to nullify. This symmetry breaks during states of emergency, where the State has expanded powers (restriction of rights, military mobilization, information control) and the people are at a structural disadvantage. Requiring the people to meet the same threshold the Legislature used to approve the emergency legislation (N3, 67% of the census) while the State operates with expanded powers produces a real inequality that contradicts the hierarchy of legitimacy principle of Article 1.

For this reason, the legislation that defines the specific scenarios for states of emergency -- what counts as a coup d'etat, who is an "attacker of the nation," what constitutes armed insurgency -- can be nullified by the people with N1 (51% of the census), regardless of the Legislature having approved it with N3. It is a calibrated compensation: the high legislative threshold (N3) makes it difficult for a faction to abuse the definitions, while the low popular threshold (N1) guarantees that the people can correct them if abuse occurs.

## Article 7: Right to Territorial Self-Determination

A territory that wants independence is, by definition, a demos: a people with its own identity and will. Even if it is a minority within the State, it is still a group of human beings whose sovereignty deserves respect. Denying the right to self-determination is denying that this demos exists, which contradicts the foundational principle of this Constitution: that sovereignty resides in the people.

Does this mean independence should be easy? No. It is reasonable and debatable to require conditions: that the territory has no pending debt with the State, that it demonstrates self-sufficiency in essential services, that it has its own military defense capacity. These requirements can be demanding. What they cannot be is indefinite in time or resolved precipitously.

Hence the two time limits. The minimum of 21 years (one generation, the same biological cycle as Article 15) guarantees that the independence movement is real and sustained, not a circumstantial impulse. The maximum of 42 years (two generations) prevents indefinite obstruction: a process lasting more than two generations is not a process; it is a denial disguised as bureaucracy.

The key is that the right to initiate the process cannot be suppressed. The conditions are negotiable; the existence of the path is not.

An open question is the level of protection of this article. Currently it is not an entrenched clause, so it can be reformed through the ordinary procedure (legislative N4 or referendum with N1 and 50% participation). This means a legislature with 75% of seats could, in theory, eliminate the right to self-determination. Should it be entrenched? The argument in favor is clear: it is a fundamental right of peoples. The argument against is that territorial independence involves factors that exceed the constitutional -- military treaties, economic agreements, international relations -- and an excessive level of protection could rigidify situations that require flexibility. For now it remains as ordinary reform, but it is a point that merits debate.

---
---

## Article 8: Equality Before the Law and Public Accountability

Parliamentary immunity is an oligarchic concept. It says: "we are above the law." This Constitution rejects it. If you voted for someone, that person is accountable to you and to the law like any other citizen. Criminal prosecution of public officials requires no prior authorization from any body. Moreover: it can be processed on a priority basis, because a corrupt public official causes more damage than a corrupt ordinary citizen.

The elimination of immunity opens a reverse attack vector: massive frivolous complaints as a tool to paralyze inconvenient public officials. This Constitution assumes presumption of innocence: a prosecuted public official continues in office until final conviction, and the regulation of procedural anti-abuse mechanisms (admissibility filters, costs for reckless litigation, sanctions for false complaints) is a matter of ordinary law. Priority processing partially mitigates paralysis by resolving cases against public officials more quickly.

Permanent disqualification for final criminal conviction is established in this article as a general principle applicable to all powers of the State. Its placement in Title I (Foundations) rather than in a specific article of a particular power avoids interpretive ambiguities about its scope. N5 protection prevents a Legislature with ordinary majority (N4) from lowering this consequence to protect convicted allies.

## Article 9: Official Language

A State needs a common language to function. Without it, laws are drafted in languages that part of the citizenry does not understand, judicial proceedings become inaccessible, and public administration fragments. The official language is not a cultural imposition: it is operational infrastructure of the State, at the same level as the electoral system or the separation of powers.

Why an entrenched clause? Because the official language is a necessary condition for all other constitutional mechanisms to function. If a Legislature could eliminate the official language through ordinary reform, it could fragment state communication as a tool of control: incomprehensible laws for part of the population, inaccessible judicial proceedings, unequal education. The common language is a democratic equalizer.

The default (the language of the previous regime) guarantees operational continuity from day one of the Transition. Without this default, there would be a gap: in what language is the AOCD published? In what language are the first elections called? The default resolves this without imposing a permanent decision -- during the Bootstrap, the Legislature can confirm or change the official language.

The N4 threshold (75%) for modifying the language during the Bootstrap is intentionally high for a Bootstrap decision. Most parameters are configured with N1, but the official language profoundly and practically irreversibly affects the entire population: changing the language of legislation, justice, and education is not a technical adjustment; it is a social transformation. N4 demands a broad consensus reflecting a genuine will, not a circumstantial majority.

Co-officiality through ordinary legislation allows the system to adapt to territorial linguistic realities without weakening the common language. A bilingual territory can operate in both languages, but the official language is always present as a guarantee that any citizen of the country can understand the laws and access justice in any territory.

---
---

# TITLE II: ELECTORAL SYSTEM

## Article 10: Single-Member Districts

Single-member representation (one district, one representative) comes from Trevijano's model. Why not party lists? Because lists turn the representative into a servant of the party, not of the electorate. In a list system, the voter chooses a party; in a single-member system, they choose a specific person whom they can hold directly accountable.

Revocation (Articles 11-12) only works with single-member representation: you cannot recall a party, but you can recall an individual. Moreover, punishing or holding a group accountable is inherently more complex and ambiguous than doing so to an individual: responsibility is diluted, blame is spread, the guilty cover for one another, and the result tends toward error and impunity. The most effective, efficient, and controllable delegation is that made to a single person.

This is the difference between delegated power and transferred power. In a list system, the citizen transfers their power to the party: once given, they do not recover it until the next election. In a single-member system with revocability, the citizen delegates their power to a specific individual and can withdraw it. Delegated power remains in the demos; transferred power leaves it. Without single-member districts, revocability is impossible or ineffective, and power is transferred rather than delegated.

A system of 1 alternate per district is recommended to guarantee continuity of representation after a revocation. The details of the alternate system are defined through ordinary law.

## Articles 11-12: Revocability and the 75% threshold

### Mathematical derivation

The 75% is not arbitrary. It is derived from the mechanics of consensus:

- In a normal election, winning requires 51% (consensus that "more than half" means legitimacy).
- To recall someone elected with 51%, it is not enough to activate the 49% that lost.
- You need to convince half of those who did vote for them, preserving the same consensual principle from which we started: that "more than half" is the threshold of legitimacy.
- Mathematics: 49% + (51% x 51%) = 49% + 26.01% = 75.01%.
- This is rounded to 75% as a fixed and universal threshold.

Furthermore, if we preserved the principle of simply obtaining 51% against to recall, it would only take convincing 2% of the population to change the result: the system would be extremely unstable. The 75% is the most stable and reasonable threshold because it incorporates the same principle of majority legitimacy but applied recursively.

### Philosophical principle

The 75% threshold creates a "political cost" of change without being tyrannical. It forces the revocation to represent an aggregation of deep social consciousness and need, not a momentary outburst of anger. No legal proof or bureaucratic process is needed: if 75% of your district wants you out, you are out. It is immunity against institutional capture of control mechanisms.

The minimum participation of 25% of the district census is identical to that of district elections (Article 13). The principle is democratic symmetry: electing and revoking are acts of equal weight, so they must require the same level of mobilization. In practice, most people do not actively participate in politics outside of electoral cycles. If a quarter of a district mobilizes specifically to recall its representative, outside the cycle and after having passed the prior filter of 10% of signatures, that is already an unequivocal signal of genuine discontent. The theoretical worst case (25% participates, 75% of those vote in favor) implies that approximately 19% of the census suffices to recall. It is a low threshold in absolute terms, but high in terms of real mobilization: getting one in five people of a district to act outside the electoral cycle requires genuine and organized discontent.

The choice of a direct, non-bureaucratic mechanism is deliberate. How many citizens in a district will truly be willing to navigate complex legal procedures, administrative deadlines, and formal requirements to determine whether they can recall their representative? In practice, bureaucracy acts as a filter that reduces participation to those who have the time, resources, and knowledge to manage it. The foreseeable result is the formation of district oligarchies: small groups that dominate the mechanisms by being the only ones who understand them. These local oligarchies may form regardless -- the Iron Law of Michels operates at all levels -- but bureaucracy would make them significantly stronger by adding a barrier to entry that only they could easily overcome.

### Census seniority and mass migration

The requirement of 2 years registered in the district to vote in a revocation is a protection against coordinated mass migration: an attacker wanting to recall an inconvenient representative would have to move thousands of people to the district and wait 2 years before they could vote. During those 2 years, those people continue voting in their previous district -- no new votes are created, only displaced with a 2-year delay.

Ordinary elections (Article 13) do not have this requirement because mass migration is less useful as an attack vector: there are local candidates who know the district, the AOCD redistributes by population every 21 years (an artificially growing district is resized), and moving thousands of people for years is an enormous cost even for a well-resourced attacker. The asymmetry between electing (without seniority) and revoking (with seniority) is deliberate: revocation is a more aggressive and concentrated act that requires additional protection against external manipulation.

## Article 13: Runoff Election

The runoff prevents capture by minorities. In a single-round system with multiple candidates, a candidate with 20% can win. The runoff guarantees that the winner has at least majority support in the final round. It is the simplest and most effective mechanism to avoid constant deadlocks and ensure a minimum level of social agreement. It is not perfect, but with the current technological and human cognitive limits, it is the best we have.

If participation does not reach the minimum of 25% of the census in either of the two rounds, the election is repeated entirely from the first round. Why not repeat only the round that failed? Because low participation in the second round may be a symptom that the two finalists do not represent the district. In a highly fragmented vote, the two top vote-getters may have 10% each -- technically the most voted, but the last choice for the remaining 80%. Repeating only the second round would force a choice between two candidates nobody wants. Repeating from the first round allows the political landscape to reorganize: new alliances, candidates who withdraw, voters who concentrate their support. The cost (repeating a first round that may have been valid) is less than the risk of imposing a representative without real support.

## Article 14: District Size and AOCD

### Why 95,000-120,000 inhabitants?

The range comes from sociolinguistic data (Trevijano): linguistic communities below a certain population threshold tend to disappear. By extension, a coherent political community needs a minimum density to maintain cultural and political identity. The range is culturally contingent, not universally derivable, but it is plausible and functional. For small countries where this range is unfeasible (such as Andorra or micronations), the Bootstrap Process allows establishing different parameters with N3 consensus. The geographic impossibility exception allows isolated districts (small islands, mountainous areas) to deviate from the range when contiguity and coherence constraints prevent it, always with the minimum necessary deviation.

### The Algorithm (AOCD)

The worst-case scenario: to capture a district through revocation, an adversary needs to influence approximately 19% of the population (75% favorable votes with minimum participation of 25% of the census). The economic proxy is the 25th percentile of income: it measures the cost of corrupting the most economically vulnerable segment.

The objective function (maximize the minimum P25 across all districts) means: the optimal distribution is the one in which the cheapest district to corrupt is as expensive as possible. The question is not "what is fair?" but "what is the structural cost of capturing this system?"

The constraints (geographic continuity, historical-cultural coherence) prevent wealth-based gerrymandering: districts cannot be drawn artificially to concentrate wealth while ignoring territorial reality.

## Article 15: 21-Year Cycle

21 years is not a political or economic number. It is biological: the human brain reaches complete cognitive maturity (specifically the prefrontal cortex, responsible for executive function, planning, and risk assessment) at 21-22 years. Each cohort of adults brings new values, interests, and worldview.

Advantages of a biological clock:

- It is not politically manipulable (the government cannot change it).
- It does not depend on economic cycles (crises or booms do not trigger redistricting).
- It is not tied to ideology (it favors neither left nor right).
- From a security perspective, it functions as a non-capturable "external clock."

Thinking as an attacker: demographic engineering requires 21-year planning horizons. The results are uncertain, making the investment unattractive for adversaries while synchronizing it with natural cycles of human generational maturation.

The 21-year cycle is protected at N5: modifying it requires broad consensus because shortening or lengthening the cycle is a significant lever of electoral manipulation. Reduction during the Bootstrap Process is not permitted because the district cycle is a structural variable that must be stable from the Constitution's birth.

## Article 16: Electoral Financing

Private donations are limited to 10% of the national P25 per person, a single donation per electoral process, and only natural persons (legal entities are prohibited from donating). Why? Because unlimited financing turns elections into auctions to the highest bidder with the largest marketing budget, reducing the richness of the democratic feedback cycle. The Iron Law of Oligarchy (Michels) predicts that the concentration of resources produces concentration of power. Limiting financing is limiting oligarchy.

The origin of donations is secret (to protect the donor from retaliation) but the destination and amount are public (so the electorate knows who receives how much). This asymmetry protects the individual without protecting the opacity of the system. For if the total donations exceed the total permitted limit, there will be a clear signal to the people that something must be investigated.

If the legal maximum is exceeded, the election is nullified once; at the second call, it is held definitively. Two chances, no more: if someone wants to sabotage elections through illegal financing, they can only delay them once. Additionally, each identified offender pays 10 times the amount exceeded, enforceable through asset expropriation if necessary. The sanction is deliberately disproportionate so that the cost of attempting to buy an election is ruinous.

The 7-day reflection period before any election prohibits all electoral campaigning. Only public events in previously agreed-upon spaces are permitted, with equal time and conditions for each candidate. Why not try to prohibit indirect propaganda with more detailed rules? Because it is unrealistic: an advertisement can use metaphors, allusions, and advocacy without mentioning logos or names, and the casuistry is infinite. The Constitution defines the limit (electoral silence with egalitarian exceptions) and leaves the details of application and sanction to electoral legislation.

# TITLE III: TRANSITION PROCESS

## Article 18: Institutional Transition

The Transition Process resolves the fundamental question: what happens the day after approving this Constitution? The democratic institutions do not yet exist, but someone has to govern while they are created. The answer is that the previous regime continues as an interim, but under the rules of this Constitution.

The previous regime exercises exclusively executive functions: maintaining order, administering services, executing existing law. It cannot legislate (the legislative monopoly belongs to the future Legislature per Article 22), nor judge (that belongs to the future Judiciary). In practice, it is a transitional government with a mandate limited to keeping the country running while democratic powers are constituted.

The election sequence is deliberate: Legislature first, Executive second. The Legislature is constituted first because it is the power closest to the people (district representatives directly elected). Once in office, the Executive is elected separately, guaranteeing its own legitimacy from day one. The Judiciary is constituted during the subsequent Bootstrap Process (Article 19), per Articles 36-38.

The publication of the AOCD with verifiable data guarantees that any citizen can replicate the calculation and verify that the districts were correctly formed. This minimizes the possibility of the previous regime manipulating the electoral distribution in its favor.

The 3-week deadline for AOCD publication, combined with elections in consecutive months, establishes an implicit ceiling of approximately 3 months for the complete Transition. It is a temporal reference for the people, not an institutional guarantee: during the Transition, the judicial mechanisms to enforce deadlines do not yet exist. The real guarantee is citizen vigilance, process verifiability, and popular pressure on a regime governing in an interim capacity.

If a state of emergency occurs during the Transition, the previous regime assumes control (it is the only actor with executive capacity before the President is elected). The mechanism is recursive: if successive interruptions occur, each time it resumes from where it was interrupted.

## Article 19: Bootstrap Process

### The hardware/software analogy

A pure constitution is too abstract to operate. A real system needs:

- Hardware: immutable principles (structure). The Constitution.
- Firmware/BIOS: initial configuration that rarely changes. The Bootstrap Process.
- Operating system: operational rules within the framework. Ordinary legislation.
- Applications: concrete policies. Day-to-day decisions.

The Bootstrap Process is the firmware: it configures the operational details that the Constitution leaves open but with limits (rights restrictable during states of emergency, specific sanctions for legislators, catalog of complementary rights, etc.) with reduced consensus levels compared to the usual post-Bootstrap levels. This allows the system to be established quickly without the rigidity of ordinary procedures.

### Why is it necessary?

Because the Constitution defines what must be protected but not how in all details. For example: it is obvious that every citizen should have the right to appeal a sentence, but not to appeal 100 times because the system would be inoperable. The exact limit depends on the specific judicial system and certain procedures, but it surely does not exceed 5 per case. The Constitution sets the minimum (1 appeal and 1 cassation guaranteed) and the maximum (5 total), but the intermediate details -- how many levels of appeal, in what types of proceedings -- are left to ordinary legislation.

The Bootstrap allows the first legislature, elected under the new Constitution, to quickly establish the operational configuration that the Constitution explicitly assigns to it (such as the minimum years of experience for judges under Article 35) with reduced consensus levels at N1, without the rigidity of ordinary procedures. Popular nullification (Article 6) operates permanently, not only during the Bootstrap: the nullification threshold always corresponds to the consensus level required for the original decision, regardless of the actual percentage that voted for it. During the Bootstrap, since the required level is N1, nullification needs 51% of the census; in normal operation, a decision whose required level is N3 needs 66% to be nullified, even if in practice 80% had approved it.

### Why can it not be reactivated?

The Bootstrap is a configuration mechanism, not a permanent tool. If it could be reactivated, any future government could invoke a "new bootstrap" to circumvent the elevated consensus levels of normal operation. It is a unique and unrepeatable event.

### State of emergency during the Bootstrap

Unlike the Transition, during the Bootstrap there already exist a democratically elected Legislature and Executive. Therefore, if a state of emergency is declared, there is no need to resort to the previous regime: the President handles the crisis per the ordinary mechanisms of Article 55. The Bootstrap simply pauses and resumes with the remaining time left as of the day before the declaration, with a minimum of 2 months. The minimum guarantees that useful configuration time always remains after a crisis, preventing a nearly exhausted Bootstrap from losing its operational capacity after an interruption.

---
---

---
---

# TITLE IV: SEPARATION AND CHECKS ON POWERS

## Article 20: Separation of Powers

The separation is material, not formal. Many constitutions declare separation of powers but allow the executive to appoint judges, the parliament to depend on the executive for its budget, or one power to control the financing of another. This Constitution requires real independence: of appointment, financing, and functioning. Without economic independence, there is no political independence.

No person may simultaneously hold more than one constitutional public office. Acceptance of a new office implies automatic resignation from the previous one. This prevents the concentration of power in a single person and reinforces the separation: a legislator cannot simultaneously be a minister, a judge cannot simultaneously be a legislator, and the President cannot self-appoint as head of a military branch.

That said, independence is not absolute nor can it be. Why? Because someone has to say "yes, this is approved." A budget, a law, an organizational structure: at some point in the process, some body must have the final word. The most logical is that the power closest to the demos -- the Legislature, composed of direct district representatives -- exercises that function of final approval. But it must do so with limits, because the people cannot be permanently attentive to every budgetary battle between powers: cognitive overload makes it practically impossible.

Hence there exist deliberate points of contact between powers, designed so they control each other without any being able to strangle the other. The clearest case is the judicial budget (Article 32): the Judiciary proposes its own budget, but the Legislature must approve or reject it. Is this a dependency? Yes, but with three protections that neutralize it as an attack vector: the Legislature cannot modify the proposed budget (only accept or reject in full), rejection requires Level N3 consensus (66%), and if rejected, the previous budget adjusted for inflation is maintained. That is, the Legislature cannot use the budget to punish the Judiciary: the worst it can do is maintain the status quo.

Mutual assured destruction (Articles 39-40) follows the same logic: it is a point of contact between Executive and Legislature that exists precisely to resolve deadlocks, but designed so that activating it has a symmetric cost that disincentivizes its abuse.

## Articles 21-23: Legislative Power

A single chamber, not bicameral. A second chamber (Senate) in a single-member system adds no representativeness: it duplicates bureaucracy and reinforces oligarchies. The legislative function is a monopoly of the Legislature (the executive does not legislate, the judiciary does not legislate), which maintains real separation of powers.

Legislative votes are public because transparency is the basis of accountability. If your representative votes in secret, you cannot hold them accountable for their votes. The publicity of the legislative vote is the necessary condition for revocation (Articles 11-12) to make sense.

Legislative consensus levels are calculated on the total number of seats, not on votes cast. There is no abstention or blank vote: whoever does not vote in favor votes against. Why? Because if consensus were calculated only on votes cast, a minority could legislate by taking advantage of absences. Worse yet: if blank voting were allowed as "I don't care," subtracting it from the calculation base, it would create an enabling mechanism with an alibi: a group of legislators could vote blank to reduce the base and allow a minority to approve laws without assuming political responsibility before their districts. With the calculation on total seats, each consensus level generates its own implicit quorum: N1 needs at least 51% of all legislators in favor, N4 needs 75%, and so on. District revocation (Articles 11-12) complements this mechanism: a representative who is systematically absent answers to their district.

The limit of 7 laws approved per week exists to protect the Judiciary. If the Legislature could approve laws without rate limitation, it could flood the judicial system with legislation faster than judges can review its constitutionality. With 7 laws per week, a judge needs to review at most 1 law per day in case of challenge. This limit ensures that the constitutionality review of Title IV is operationally viable, not just theoretical.

## Articles 24-25: Executive Power

The President is directly elected by the people. Why not by parliament? Because direct election is simply more democratic: although the Legislature is composed of district representatives close to the citizen, it would still be an indirect election, one more step between the demos and whoever manages the State. Direct election of the Executive gives the President their own legitimacy, independent of the Legislature's, which reinforces the separation of powers. But the President is a pure manager: they execute the laws the Legislature approves, not create them. The distinction is fundamental. In many parliamentary systems, the prime minister is the leader of the majority party, which merges executive and legislative. Here they are radically separated.

There is only one figure at the helm of the Executive: the President. No simultaneous prime minister and president, no heads of government separate from heads of state, no intermediate figures that dilute responsibility. Each added layer increases ambiguity about who decides what, multiplies bureaucracy, and makes the system unnecessarily complex. With a real and controlled separation of powers like this Constitution's, there is no need to distribute the Executive among several figures: a single individual in command, with direct popular legitimacy, revocable through mutual assured destruction if the Legislature deems it necessary. Responsibility is clear, the chain of command is simple, and there is no ambiguity about whom to hold accountable.

Ministerial delegation functions as proposal, not autonomy: ministers prepare and propose decisions, but every Executive Power decision requires the President's approval for execution. There is no figure of the minister who acts and then the President revokes: nothing is executed without prior approval. Why not allow ministerial autonomy with presidential override? Because a captured minister could act irreversibly before the President intervenes. With the prior approval model, the attacker needs to capture the President, not a minister. This is slower but safer.

Military decisions (Articles 50-52) and the declaration of states of emergency (Article 55) are functions of the President like any other, but their specific articles directly regulate how they are made: a clear chain of command with a single identifiable responsible party, which is necessary for the structure of personal consequences (especially the amputation of Article 52) to function.

The presidential term (5 years) is intentionally different from the legislative (4 years) to decouple electoral cycles and prevent the same moment of enthusiasm or crisis from simultaneously determining both powers.

The term limit is a cooldown, not a lifetime prohibition. Why? Because a lifetime limit is paternalistic: if the people want to re-elect a leader who has demonstrated competence, preventing it substitutes an arbitrary rule for popular judgment. The cooldown of one complete term (5 years out of office) fulfills the real defensive function: breaking the continuity of power to prevent progressive institutional capture, without permanently closing the door on a good ruler. The classic attack vector against this model is the puppet: the outgoing leader installs an allied successor during their absence. But in this Constitution, the successor is not installed; they are elected by direct suffrage. And if they turn out to be an incompetent puppet, the mechanisms of revocation (mutual assured destruction, Article 39) and judicial control operate against them with the same force as against any other President. Trusting the mechanisms for this is consistent with trusting them for everything else.

## Article 26: Presidential Succession

The Vice President is appointed by the President, not elected by the people. This is deliberate: their function is not to govern but to guarantee operational continuity in case of emergency. Precisely because they have no direct popular legitimacy, their interim mandate must be as brief as possible: new elections within a maximum of 45 days. Whoever assumes the interim Presidency is subject to exactly the same responsibilities, obligations, and consequences as the elected President. This is fundamental: the interim is not a guardian with special immunity; they are a President with all the force of law.

Why not let the Vice President finish the term? Because that would be handing over Executive Power to someone nobody voted for, potentially for years. This opens two attack vectors: assassinating the President so their Vice President (who has been bought) assumes power, or a foreign power corrupting the Vice President knowing they only need to eliminate the President for their investment to pay off. Immediate elections neutralize both vectors: even if the Vice President has been bought, they only have 45 days before the people decide who governs.

If elections are not held within the 45-day period, the interim is considered a usurper. This is deliberate: the interim has no legitimate incentive to delay elections, so any delay is suspicious. The consequence is severe precisely so no one takes the risk. The only exception is a state of emergency that materially prevents elections, a case covered by Article 61, which suspends electoral deadlines when the conditions of Article 5 cannot be guaranteed. Article 26 explicitly references Article 61 to prevent an isolated reading of Article 26 from leading to an interpretation of the deadline as absolute.

When succession is activated by mutual assured destruction (Article 39), the interim Vice President has strictly limited functions: maintaining institutional order, without new budgets, appointments, or policies. Why more severe restrictions than in succession by incapacity? Because mutual assured destruction is a deliberate political act, not an emergency. The country does not need a new government; it needs new elections. The interim is a guardian of the status quo, not a ruler.

The death of the President activates succession directly (Article 26), without judicial process. It is an objective fact that requires no declaration by a judge nor admits appeal -- requiring judicial procedure for an evident death would introduce an absurd delay in the chain of command.

The declaration of incapacity (Article 27) is exclusively judicial and is reserved for clinically disputable states: coma and severe cognitive deterioration. The process can be initiated by the Vice President or by the Legislature through N2 consensus. The Vice President can initiate the process unilaterally, which creates a conflict of interest (they become interim and candidate). However, the Vice President does not declare the incapacity -- they only request it. The judge acts as a filter, and the declaration is challengeable by any citizen with the right to vote. If the declaration is overturned on appeal, the judge is subject to the sanctions of Article 44 (criminal liability of judges for overturned incapacity declarations). These counterweights -- judicial filter, citizen appeal, sanction of the judge -- make it unnecessary to require an additional legislative threshold for the Vice President's request, which would delay the mechanism in real emergencies.

The declaration of incapacity takes immediate effect -- it is not suspended during appeal. A President in a coma needs to be replaced immediately; they cannot wait weeks of process. If the declaration is overturned afterward, the judge pays the criminal consequences. The balance is: speed of response with posterior control, not prevention that paralyzes.

If the President recovers their capacity before new elections are held, they retake office automatically. If new elections have already been held, the new President is legitimate -- they were elected by the people. There is no restitution mechanism: the democratic election is definitive, regardless of whether the incapacity was real or erroneous. The remedy against an erroneous declaration is the sanction of the judge (Article 44), not the annulment of a democratic election.

The causes of incapacity are expandable but not reducible by the Legislature with N3 (during Bootstrap, N2), which allows adapting the causes to unforeseen situations without lowering the guarantees. Irreducibility prevents a complicit Legislature from eliminating causes of incapacity to protect a sick President whom it suits them to keep.

The secondary line of succession (longest-serving Legislative representative) covers the extreme case of both President and Vice President being simultaneously incapacitated. The same conditions apply: interim character, same responsibilities and consequences, elections within 45 days. The line of succession is expandable but not reducible by the Legislature with N3 (during Bootstrap, N1), allowing additional positions to be added to the succession chain if experience so advises. Irreducibility is key: it prevents a complicit Legislature from shortening the succession chain to facilitate a controlled power vacuum.

## Articles 28-31: Ministries and Budget

The limit of 20 ministries and the default budget mechanism are mutually reinforcing measures. The limit on ministries prevents bureaucratic inflation: each ministry is a center of power and budget, and more ministries means more capture points for an adversary. The President has a monopoly on appointment (they do not need parliamentary approval for ministers) because the executive must be agile. The limit is modified through the ordinary reform procedure (N4): it is an administrative detail that does not merit reinforced protection. During the Bootstrap it can be adjusted with N1 to adapt the initial ministerial structure.

The automatic removal of a minister upon criminal conviction requires that the conviction be final -- that is, confirmed on appeal or not challenged within the deadline. Without this requirement, a corrupt first-instance judge could automatically remove any minister with a fabricated conviction, knowing it will be overturned on appeal but that the damage (the removal) will already be done. The word "final" guarantees that the complete judicial system has confirmed the conviction before irreversible effects occur, consistent with the right of appeal under Article 34 and with the terminology of Article 4 ("final criminal conviction").

The default budget complements this agility with stability: if the Legislature does not approve a new budget, the previous one adjusted for inflation is extended. The system always works; political disagreement does not paralyze the State. Together, both measures limit the size of the executive structure (maximum 20 ministries) and guarantee that this structure always has operational funding (default budget).

A President cannot inflate the bureaucracy to create power fiefdoms, and a Legislature cannot paralyze the government by withholding the budget as a political weapon. The only remaining attack vector is the manipulation of inflation data to indirectly increase the executive budget, but falsifying inflation has visible and immediate consequences for the entire citizenry, which generates a natural counterweight: popular anger acts as a correction mechanism. Inflation is one of the few macroeconomic data points that citizens perceive directly in their daily lives -- in their grocery shopping, in their rent, in energy prices -- without needing to read reports or understand statistics. A gross manipulation would be evident; a subtle manipulation (1-2% extra) produces a marginal benefit that does not justify the political risk of being discovered. This is a consciously accepted risk: constitutionalizing statistical methodology would be over-engineering, and the Legislature can always approve a new budget that corrects any deviation.

## Articles 32-38: Judicial Power

### Financial independence

The Supreme Court proposes its own budget. Any justice can submit a proposal, but the agreement of 2/3 of the justices is required to present it to the Legislature. This internal threshold prevents a court president or a minority of justices from unilaterally proposing an abusive budget -- and it is consistent with the 2/3 already used for accreditations under Article 35. If the justices cannot reach agreement, the previous budget adjusted for inflation is maintained: lack of internal consensus does not paralyze Judicial funding.

The Legislature can approve or reject the proposed budget (with Level N3 consensus), but not modify it. If rejected, the previous one adjusted for inflation is maintained. The judicial budget thus has a dual control: 2/3 internal to propose and N3 external to reject. The N3 rejection level is protected at N5, consistent with the other judicial parameters: without this protection, a Legislature with N4 could lower the rejection threshold to N1 and financially strangle the Judiciary with a simple majority.

### Three-level structure

First instance, appeal/cassation, and Supreme Court. The three-level structure is protected at N5 because Articles 34 and 43 depend on the existence of exactly these three levels -- modifying the structure requires rethinking the entire system of appeals and constitutionality review.

The Constitution guarantees a minimum of one appeal (full review of facts and law) and one cassation (review only of law) before the immediately superior court. "Immediately" is deliberate: appeals always go to level +1 (first to second, second to Supreme), never skipping a level. The total maximum of appeals and cassations in a single case is 5.

Decisions of the Supreme Court are final by default. Only when the Constitution expressly establishes it (such as presidential noncompliance under Article 41 or the accountability of Article 52) is a Supreme Court decision appealable. In those cases, the appeal is resolved by a different justice of the same Court, selected through a deterministic random mechanism based on the appellant's biometric data. This mechanism prevents the appellant from choosing which justice will review their case -- the assignment is deterministic and verifiable, but not manipulable. The constitutionality process of Article 43 has its own layer system (first instance, cassation, Supreme Court) that functions as a specific procedure, replacing the general regime of Article 34 for constitutionality questions.

### Appointment of ordinary judges and accreditations

The appointment of first and second instance judges is the exclusive competence of the Judiciary. Neither the Executive nor the Legislature participates in the process. The qualification exam is designed, administered, and graded by the Judiciary. The reason is direct: whoever controls the entry gate to the judicial system controls the judicial system. An already-appointed judge is independent, but if another power decides who enters, independence is nominal.

Valid degrees and accredited law faculties are determined by 2/3 of the Supreme Court. The 8-year modification cycle prevents opportunistic changes (discrediting a faculty that trains inconvenient judges). The 1-year transition period protects those who have just graduated under a current accreditation. During the Bootstrap, all faculties of the previous regime are accredited by default; after the first round of justices, the list can be adjusted with N1 of the Supreme Court to allow an initial calibration without requiring the full 2/3 threshold.

Candidates for the Supreme Court must demonstrate a minimum of 5 years of experience as a judge (adjustable between 5 and 10 years). This requirement does not apply to ordinary judges, where it would be paradoxical to require judicial experience of someone who is not yet a judge. For ordinary judges, the degree and exam suffice; for the Supreme Court, experience is added because their decisions are final in the judicial order.

### Supreme Court: composition and renewal

Article 36 defines the composition (9 justices, 12-year terms, 8-year exclusion, staggered renewal of 3 every 4 years) and Article 38 the procedures for initial constitution and renewal. This separation follows the single responsibility principle: Article 36 says WHAT the Supreme Court is, Article 37 says WHO composes it, and Article 38 says HOW it is constituted and renewed.

Why staggered renewal? The justices are elected by vote of legal professionals, not appointed by the government. Staggering does not protect against "government capture" in the classic sense -- it protects against waves. A wave of opinion, propaganda, or vote buying at a specific moment can only affect one-third of the court. Capturing the majority requires maintaining that influence for three consecutive cycles (12 years), which is much more difficult and expensive than capturing it all at once.

The numerical parameters (9, 12, 8, 4, 3) are protected at N5. The coherence of staggered renewal -- that the number of justices be divisible by the number renewed per cycle -- is protected at N6. This mathematical constraint guarantees equal cohorts: without it, someone could change to 10 justices while maintaining 3 per cycle, creating unequal cohorts (3, 3, 4) with one cycle renewing more justices than the others -- a capture window.

### Appointment of Supreme Court justices

Candidates are proposed by legal institutions (bar associations, law faculties, judges' associations). The final election is conducted by legal professionals through direct, binding, and non-delegable voting. Why not popular vote by the entire citizenry? As Trevijano argued, the selection of judges is a technical matter: the average citizen lacks the criteria to evaluate legal competence -- they would vote by name, charisma, or campaign, not by legal rigor. Legal professionals do have that criteria.

A smaller professional electorate is more vulnerable to vote buying than millions of citizens. This is where staggered renewal acts as complementary protection: even if an attacker buys votes in one cycle, they only capture one-third of the court. And legal professionals tend to have medium-to-high incomes, which makes buying them more expensive. The combination of professional electorate + staggering offers technical criteria without sacrificing protection against capture.

The total number of candidates must be strictly greater than the number of vacancies -- without this constitutional minimum, the Bootstrap could configure a system with exactly as many candidates as positions, turning the election into a mere ratification without a real option. The definition of who qualifies as a legal professional is established during the Bootstrap with N1. The voting procedure (number of candidates per institution, voting system) is established with N2 -- a higher threshold than usual in the Bootstrap because it determines how the body that interprets the Constitution is selected. Any subsequent modification requires N5.

### The verifiable random draw for initial terms

During the Bootstrap, the 9 justices are simultaneously appointed but need staggered terms. The specific draw procedure is chosen during the Bootstrap with N1, provided it is deterministic, non-manipulable, and publicly verifiable. If no alternative procedure is chosen, the default method applies: a cryptographic hash function applied to each justice's biometric data, with a fallback chain that guarantees availability for any person regardless of physical disabilities.

Why offer a default method? For operational reasons: having a concrete procedure already defined makes the Bootstrap Process more fluid. Following the philosophy of Articles 5 and 17, what the Constitution protects are the characteristics (deterministic, non-manipulable, verifiable), not the technology. Outside the Bootstrap, the draw procedure cannot be modified -- it is used only once and the rotation can only be manipulated at the start.

### Early vacancies

If a justice leaves office before their term expires (death, resignation, disqualification), the replacement serves only the remaining time of the original term. Why not a full 12-year term? Because that would break the staggered renewal: if a justice from cohort A dies in year 2 and their replacement serves 12 full years, cohort A falls out of sync with the others. Eventually renewals accumulate and one cycle allows more justices to be appointed than intended -- a capture window. That the replacement may serve only 2 weeks (if the vacancy occurs at the end of the term) is a minor inconvenience compared to breaking the systemic protection of staggering.

While the vacancy is not filled, the empty seat is counted as a vote against in Supreme Court decisions requiring consensus, consistent with the rule of Article 23 for legislative seats. This makes the court's decisions more difficult during the vacancy, which functions as a natural incentive to fill it quickly.

---
---

## Articles 39-40: Mutual Assured Destruction

How to resolve a deadlock between President and Parliament without destroying democracy? The mechanism of mutual assured destruction, an original idea of Trevijano, solves this problem: both have a "nuclear button." The Legislature can remove the President, and the President can dissolve the Legislature. But activating the button destroys both: simultaneous elections are called for both. It is mutually assured destruction (MAD), inspired by nuclear deterrence.

It works because the cost of use is symmetric: both lose power, so it is only activated in a genuine crisis, not capriciously. Neither branch can tyrannize the other because there is no veto imbalance. And the outcome is always democratic: the people decide who was right through new elections.

The deactivation period (cooldown) is a proprietary addition to Trevijano's idea. After activating the mechanism, there is a period during which it cannot be used again, and this period is asymmetric: the invoker pays more (longer period before being able to reactivate it). This disincentivizes offensive use and favors defensive use. Without this cooldown, the mechanism could become a weapon of attrition: activating it repeatedly until the adversary surrenders. The asymmetric cooldown turns it into a weapon of last resort.

The existence of the mechanism is an entrenched clause (Article 66): it cannot be eliminated. Its numerical parameters (removal threshold, temporal range limits, cooldown periods) require N6 consensus to modify and are not modifiable during the Bootstrap -- the structure of the mechanism must be stable from day one. The only exception is the specific value of the deadline for calling new elections, adjustable within the range of 7 to 30 days: with N1 during the Bootstrap and N4 afterward. The logic is the same as in a competitive game: not only does the ability matter, but the cooldown and activation parameters are equally determinative of its effectiveness. Changing the removal threshold from N1 to N6 would be equivalent to neutralizing the mechanism without formally eliminating it.

No participant is excluded from running in the immediate elections. Why not prohibit the removed President from running? Because that would be removing the people's option to re-elect them, and this Constitution never restricts the people's options. If the Legislature removes the President but the people want to re-elect them, that is democracy working. If the President dissolves the Legislature and runs again, the people decide whether they were right. The cost of the mechanism is not the exclusion of candidates but the electoral uncertainty and the asymmetric cooldown: the invoker risks losing power and pays a longer deactivation period.

During the period between activation and the new elections, the Legislature remains dissolved and cannot legislate. However, if a state of emergency occurs during that period, the dissolved Legislature is reconvened exclusively to exercise the control functions of Articles 58 to 63. Why this exception? Because without it, a corrupt President could invoke destruction and a foreign ally could fabricate a military situation during the following 30 days: the military state of emergency activates automatically, the interim Vice President obtains emergency powers, elections are postponed indefinitely, and there is no Legislature to revoke anything. The limited reconvention closes this loophole without restoring general legislative powers.

## Grave Presidential Noncompliance

Mutual assured destruction resolves deadlocks between Legislature and Executive. But what happens when the President ignores the Judiciary? A President who refuses to execute a final ruling of the Supreme Court is breaking the separation of powers, and if the Legislature is complicit or indifferent, mutual assured destruction is not activated.

This mechanism closes that gap: both the Legislature (N1) and the People (10% of the census) can initiate a process before the Supreme Court to determine whether the noncompliance is serious enough to call new presidential elections. Responsibility falls on the President because every Executive decision requires their approval (Article 25) -- if a subordinate fails to comply, the President is responsible for having approved or permitted it. The minimum constitutional cause (refusing to execute a final Supreme Court ruling) cannot be eliminated or modified; additional causes are established by ordinary legislation with N4 protection. The access parameters for the mechanism (N1 and 10%) are protected at N6, consistent with mutual assured destruction: they are control mechanisms whose accessibility cannot be neutralized without quasi-unanimity.

Why new elections and not imprisonment? Because the problem is not criminal but democratic: a President who ignores the Judiciary has broken the pact of separation of powers, and the democratic response is to return the decision to the people. If they have also committed a crime, the ordinary criminal avenue remains available. The effect occurs only when the Supreme Court's decision becomes final -- that is, after the appeal that Article 34 allows or after the deadline expires without challenge. The interim exercises the limited functions of the second scenario of Article 26 (maintenance of institutional order), for the same reason as in mutual assured destruction: the VP served under a President removed for noncompliance and should not be able to continue the same policies.

## Why diffuse review and not a centralized Constitutional Court?

The traditional Constitutional Court (European model, concentrated) is:

- A new bureaucratic super-institution.
- Easily capturable: it suffices to control a single body to control all constitutional interpretation.
- A single point of failure for democracy.

Diffuse review (American model, distributed) allows any judge to declare a law inapplicable as unconstitutional in a specific case. Combined with the layer system (first instance -> cassation -> Supreme Court -> popular nullification), the power of constitutional review is distributed without concentrating it in a single body.

### Saturation of the constitutional review system

The system allows a maximum of 100 laws under simultaneous review (10 groups of 10). The 6-year blocking period per law (counted from the filing of the challenge) and the 4-month waiting period per citizen are the two protections against deliberate saturation.

An attacker attempting to saturate the system needs:
- At least 10 coordinated citizens to fill all 100 slots at once (10 groups of 10 laws)
- Those citizens cannot file challenges again for 4 months
- To maintain saturation continuously: at least 40 citizens (10 for each month of the waiting period)

Each month of complete saturation consumes approximately 100 challengeable laws (blocked for 6 years). If L is the total number of laws in force and approximately 364 new laws are approved per year (7 per week), the maximum duration of complete saturation is approximately L / (1,200 - 364) ~ L / 836 years. For a legal system of 10,000 laws, complete saturation could be maintained for about 12 years; for 1,000 laws, barely over a year.

Once existing challengeable laws are exhausted, the attacker can only challenge new laws (364/year), which fills less than a third of the system's capacity (364 of 1,200 possible per year). Complete saturation becomes mathematically impossible.

This is an accepted risk: temporary saturation is possible but costly (requires coordination of dozens of citizens), limited in time (challengeable laws are exhausted), and partially mitigated (the system continues functioning at 70% after the initial exhaustion).

All numerical parameters of Article 43 are protected at N5. They are not protected individually because they form an interrelated system: the 6-year blocking period, the 10 groups of 10, the 2-week appeal deadlines, and the 4-month waiting period per citizen are calibrated as a joint balance. Changing any of them alters the balance between system accessibility and protection against saturation.

## Bidirectional criminal liability

Article 44 centralizes the criminal liabilities arising from the constitutionality process. It is bidirectional in two senses: it sanctions both legislators who approve unconstitutional laws and judges who err in ruling on constitutionality -- in either direction. A judge who declares a constitutional law unconstitutional and a judge who lets an unconstitutional law pass bear the same responsibility. A judge is obligated to rule; they cannot evade the decision, so they must be accountable for being wrong in either direction.

The review of judicial error is conducted through the procedure of Article 43 but applying the constitutional text and configurations in force at the time the decision was issued. This is fundamental: if the Constitution is reformed between the decision and the review, the judge cannot be punished for correctly applying the Constitution of their time.

The criminal liabilities for other mechanisms (popular nullification under Article 46, presidential incapacity under Article 27) are defined in their respective articles, referencing Article 45 for the specific sanctions and Article 44 as a benchmark of severity. Each mechanism manages its own consequences.

The specific sanctions (Article 45) are established during the Bootstrap with N3 -- a higher threshold than the usual N1 because defining criminal penalties deserves broad consensus. The default sanction for legislators is the payment of 10 years of their salary as debt, applicable if the Bootstrap does not define another. For Supreme Court justices, the constitutional minimum sanction is 20 years of imprisonment, configurable during the Bootstrap with N3 and modifiable subsequently with N5.

The economic sanction can only be paid with salary from personal labor (not investments, donations, or asset sales). This prevents a wealthy person from easily paying the fine and turning it into a business cost.

## Popular Nullification of judicial decisions (Article 46)

When the Supreme Court declares a law unconstitutional, its decision is technically final in the judicial order. But it is not democratically final. The people, as the ultimate source of legitimacy (Article 1), can nullify that decision through collecting signatures of 51% of the census. This implements the hierarchy of legitimacy: Judicial < Legislative < Popular.

The 3-month reflection period avoids impulsive reactions. The threshold of 51% of the census (not of voters) guarantees that the nullification represents a real majority of society, not just of those mobilized.

Popular nullification also extends to ordinary (non-constitutional) judicial decisions, with higher thresholds: 30% of the census as the initiating group and signatures at the consensus level equal to the highest level required to approve the laws on which the decision was based, with a minimum of N1. This is consistent with the hierarchy of Article 1: if the people created a law with a certain consensus level, they need at least that same level to contradict the judicial interpretation of that law.

The signature collection must be formally declared before it begins -- signatures prior to the declaration are not valid. This prevents the silent accumulation of signatures as a form of permanent pressure on the Judiciary. Once declared, the maximum period to complete the collection is 2 years. All parameters of the article are protected at N6, consistent with the fact that popular nullification is a mechanism of direct democratic control whose accessibility cannot be neutralized without quasi-unanimity.

---
---

## Why is budgetary transparency constitutional?

Because without it, all other mechanisms are blind and inefficient, probably to the point of being inoperative.

Revocation requires information about what your representative does. Verifying that money goes where the law says it should requires access to the actual budget. Post-emergency accountability requires access to real data. Budgetary transparency is the informational infrastructure of democracy.

Every public budget is published in an auditable system. Budget execution is updated every 30 days. Exceptions are minimal and limited (classified intelligence operations, audited by a legislative commission).

## Right of citizen audit

Any citizen can request public data and receive it within a maximum of 30 days. This deadline is constitutional (not legislative) so that no subsequent law can extend it indefinitely. The process must be accessible, free of charge, and comprehensible: it is not enough to publish data in an incomprehensible technical format.

---
---

## Civil control of the military

Due to the frenetic nature of battle, a military with several leaders of equal authority is like a headless chicken: contradictory orders, paralysis in decisions, and confusion in the chain of command. That is why military command requires a single supreme commander. The Constitution assigns this role to the President because military power must be subordinated to civilian power -- an autonomous military is a state within a state -- and the President is the civilian office most directly linked to the people by direct election.

## Why 85% (N5) to declare war?

This extraordinarily high threshold is intentional: it seeks to limit wars of aggression. Only a war that enjoys near-unanimous national consensus can be declared. The initiative is exclusive to the President (they are the Commander-in-Chief), but approval belongs to the Legislature -- neither can declare war unilaterally. Immediate defense against attack does not require prior declaration (it would be absurd to demand a vote while bombs are falling), but it does require immediate notification to the Legislature and subsequent accountability. Ordering a defense without a real attack is punished with the same severity as the disastrous secret operations of Article 52 -- personal and physical punishment. This closes the loophole of a President who fabricates an attack to activate a military state of emergency.

Revoking the declaration of war requires N3 of the Legislature (on the initiative of the President or of the Legislature itself), provided the territory is not under attack. Why N3 and not N1? Because declaring war is a gravely serious decision made with N5 -- revoking it with a simple majority would trivialize that commitment. N3 demands broad consensus to end the war, preventing a circumstantial majority from abandoning an active conflict under political pressure. The condition of not being under attack prevents unilateral surrender: while the enemy is attacking, the armed forces need the powers of the military state of emergency to defend the territory.

This accountability exists, among other things, to mitigate the scenario in which a president deliberately orders their forces to let themselves be attacked in order to attempt to concentrate power in their own hands. It may be paranoid, but the goal of this Constitution is to last forever if possible, and every scenario must have, if not a fix, at least a damage mitigation. Here we again observe the design mindset of robust systems that every hacker and software architect shares: good will is not assumed, nor are "happy paths" -- failure is assumed.

## Amputation of a hand for disastrous secret operations

This is the most controversial provision of the Constitution. Secret operations are a very useful military weapon and therefore should not be prohibited, but they need a counterweight proportional to their opacity. The logic is as follows:

The President can order secret military operations without legislative approval (that is what makes them secret). But if the operation results in military disaster or unauthorized armed conflict, the President personally responds with their body. The process maintains the separation of powers: the Legislature accuses (with N1), but the Supreme Court judges and decides whether to apply the punishment. The decision is appealable by any citizen, like any other judicial decision.

Why physical punishment and not imprisonment or a fine?

- Money can buy anything. A president who initiates a secret war through foreign bribery accepts the risk of a fine or imprisonment if the economic benefit is sufficient. Irreversible physical pain has no economic payoff: it only has cost.
- Imprisonment can be evaded (pardon, escape, statute of limitations). Amputation is immediate and irreversible.
- The deterrence works because it is personal. No abstract institution is punished; the individual who made the decision is punished.

From incentive analysis: if foreign nations attempt to buy a president to create chaos, they cannot buy them out of the pain. The personal cost guarantees that the President will carefully weigh before ordering risky operations without legislative backing.

Amputation is the default punishment, but it can be modified during the Bootstrap with N3 provided the alternative punishment is personal and physical -- not economic or substitutable. This flexibility allows adapting the specific form of punishment to cultural sensitivities without weakening the deterrent principle.

## Separation of military branches

The Armed Forces are organized into separate branches (Army, Navy, Air Force) with chiefs appointed by the President and revocable by the Legislature (N4). This separation makes coups d'etat more difficult: simultaneous coordination across all branches would be needed, which multiplies the number of people who must conspire and increases the probability of leaks. The protection is not absolute -- the President is Commander-in-Chief of all branches -- but each branch chief is an independent point of failure who can refuse to participate.

The three original branches cannot be eliminated or merged (N5 to modify this protection). The Legislature can create new branches with N3 to adapt to technological evolution (cyberdefense, space forces) without weakening the anti-coup structure. Specialized subdepartments (chemical weapons, cybersecurity) can be created within each branch without needing a new branch.

After revoking a branch chief, the President must appoint a replacement immediately but cannot revoke them for 1 month (except during a state of emergency). This prevents the cycling of chiefs to find a yes-man. The replacement cannot be the revoked person, nor a relative up to the second degree of the President, nor the Vice President, nor a serving minister -- restrictions that close the vectors of nepotism and concentration of civilian-military power.

---
---

## The structural problem

Emergency powers tend to become permanent. It is a predictable pattern from incentive analysis: whoever receives exceptional powers has the incentive to maintain them, and the crisis itself provides the justification for not returning them. As stated above, protection has a double edge.

Without explicit mechanisms of expiration and increasing consensus, every emergency becomes an opportunity for authoritarianism. There is no need to search for specific historical examples, though they exist: it suffices to understand the incentives. If you give someone power without a return date, they will probably not return it or will cling to it as long as they can.

Whatever the frequency of this phenomenon, a serious and functional Constitution must take even the smallest detail into account. Just as irreversible cryptocurrency code -- where you cannot patch after deployment -- a Constitution must anticipate failures before they occur. Here we can observe the principle mentioned earlier: good will is not assumed; failure is assumed.

## Increasing consensus and decreasing intervals

Renewal of the state of emergency requires increasingly higher majorities at increasingly shorter intervals:

- At 6 months: 51% (easy if the crisis is real).
- At 8 months: 60% (questions begin).
- At 9 months: 66% (serious debate).
- At 10 months: 75% (broad consensus required).
- Every 2 weeks afterward: 85% (near unanimity).

The logic is simple: a legitimate crisis easily generates consensus. A pseudo-crisis loses support over time. If a government needs 7-10 months of emergency powers, society has the right to question it with increasing rigor.

## False declaration of a state of emergency

Declaring a state of emergency without a real crisis is a serious crime (10 years of imprisonment by default). The reason is obvious: a state of emergency temporarily concentrates power in the Executive. If there are no consequences for declaring one falsely, it becomes a tool for concentrating power under the pretext of crisis. The default sanction is high but modifiable (N2 during Bootstrap, N3 afterward) because it is an operational parameter whose optimal value depends on context.

## Automatic activation

In the fields of Internal Security and Military, activation is automatic: the state of emergency exists as a legal fact from the moment the cause occurs, not from when someone declares it. There is no prior filter at entry. This is deliberate: faced with a coup d'etat or an invasion, conditioning activation on a formal act by an official who could be compromised or incapacitated is worse than having no filter. Controls are at the exit: legislative ratification (Internal Security), judicial review (Art 62), crime for falsity (Art 55), and accountability (Art 64).

## Specific scenarios and definition of "attacker of the nation"

The causes for each type of state of emergency (natural catastrophe, coup d'etat, invasion) are necessarily generic in the constitutional text. It is impossible to anticipate every specific scenario: is a massive cyberattack a "technological disaster" or an act of "war"? Is a violent protest "armed insurgency"? Attempting to enumerate every case in the Constitution guarantees gaps.

The solution is to delegate the definition of specific scenarios to ordinary legislation, but with a high threshold: N3 (67% of the Legislature). This level is deliberately higher than the usual N1 or N2 for ordinary legislation because these definitions determine when the State can restrict fundamental rights. A low threshold would allow a simple majority to define "coup d'etat" in a way that includes peaceful protests or "attacker of the nation" in a way that includes political opponents. N3 demands a broad consensus that makes the partisan use of these definitions difficult.

The same logic applies with particular force to the definition of "attacker of the nation" in the Military Field, where all fundamental rights can be restricted. History repeatedly shows that governments label opponents as enemies of the State to justify repression. N3 does not eliminate this risk, but it substantially makes it more difficult. And if it happens anyway, the popular nullification exception of Article 6 allows the people to correct it with only N1 of the census.

## Six non-suspendable limits

No crisis authorizes:

1. Modifying the Constitution.
2. Changing the electoral law.
3. Postponing elections (except for physical impossibility).
4. Postponing judicial proceedings (except for physical impossibility).
5. Governing without parliament.
6. Governing without courts.

These limits are absolute because if you destroy any of them, democracy crumbles -- more slowly or more quickly, but it crumbles. Without a stable constitution, there are no rules. Without electoral law, there are no clean elections. Without elections, there is no representation. Without parliament, there is no democratic legislation. Without courts, there is no one to control power. Each of these six points is a structural piece: remove one and the rest weakens until collapse.

## Parliamentary control and elections during states of emergency

The Legislature functions normally during any state of emergency (limit 5). Mutual assured destruction is suspended because it makes no sense to resolve a political deadlock while there is a real crisis -- but the Legislature continues legislating, overseeing, and controlling.

Elections can only be postponed due to objective physical impossibility (aligned with Article 63). It is not enough that "conditions cannot be guaranteed" -- that threshold was too low and left the Executive the decision of when conditions were guaranteed, creating a perverse incentive to prolong the suspension. Now the Legislature determines through N1 when the physical impossibility has ceased. Once determined, the 45-day deadline to hold elections (the same as Article 26) begins to run and the usurpation penalty is reactivated. The same 45-day deadline as in ordinary presidential succession is used to avoid having two different deadlines for the same type of decision. This eliminates the possibility of the Executive being judge and party on the duration of its own interim mandate.

## Judicial control of the state of emergency declaration

The Judiciary can review not only the measures adopted during the emergency but the declaration itself: did the crisis really exist? Any citizen with the right to vote can request this review before a first-instance judge, without needing to have had their rights violated. This is deliberate: the declaration of a state of emergency affects the entire citizenry, so any citizen has standing to challenge it.

If a court declares through a final ruling that the state of emergency was declared without a real crisis, the state of emergency ceases automatically (Article 65). This closes the last gap in the termination mechanisms: without this provision, a fraudulently declared state of emergency could only end through non-renewal by the Legislature or through legislative revocation -- both political controls. Judicial review adds an independent counterweight based on facts, not politics.

## Prohibition of decrees outside of states of emergency

The Executive can only issue decrees during a state of emergency. Outside of one, decrees are absolutely prohibited. This prevents executive legislation ("decree-ism") that erodes the separation of powers. If the President wants a law, they must ask the Legislature for it. And when decrees are issued, Article 60 subjects them to three limits: they can only cover measures from a closed list by type of emergency, they cease automatically when the state of emergency ends, and under no circumstances can they annul or modify the Constitution.

---
---

---
---

# TITLE V: REFORM AND CONSTITUTIONAL PROTECTION

## Why these twelve specific entrenched clauses?

The entrenched clauses protect the pillars without which democracy ceases to be democracy:

1. Popular sovereignty (Article 1): without it, power does not reside in the people.
2. Hierarchy of legitimacy (Article 1): without it, a subordinate power can capture the superior one.
3. Universal suffrage (Article 4): without it, not everyone participates.
4. Vote guarantees (Article 5): without secrecy, the vote is coercible; without verifiability and auditability, fraud is undetectable.
5. Guarantee of popular nullification (Article 6): without it, the people lose the ability to correct errors of delegated power.
6. Equality before the law (Article 8): without it, rulers become a privileged class immune to the consequences of their actions.
7. Official language (Article 9): without at least one shared official language, legislation, justice, and administration cannot function uniformly or accessibly for all citizens.
8. Separation of powers (Article 20): without it, power concentrates.
9. Balance of powers (Article 39): without mutual assured destruction, one power can indefinitely subjugate the other without consequences.
10. Constitutional supremacy (Article 42): without it, an ordinary law can hollow out the Constitution's content.
11. Right and procedures of reform (Articles 67 through 69 inclusive): without them, the Constitution becomes a tyranny of the dead over the living. The clause protects not only the right to reform but also the procedure for reforming entrenched clauses (Article 67), preventing an attacker from lowering the thresholds of the entrenched procedure via ordinary reform.
12. Fundamental democratic rights (Article 71): without them (expression, information, assembly, integrity, vote privacy), the democratic mechanisms work on paper but not in practice.

What is not an entrenched clause: administrative details, numbers of representatives, specific procedures. These can evolve without destroying democracy. The distinction is clear: the entrenched protects the existence of fundamental mechanisms; the numerical parameters of those mechanisms are protected through specific consensus levels (N5, N6) that allow adjustments without eliminating the mechanism itself.

## Temporal asymmetry

Democracy has an inherent paradox: giving power to the people means also giving them the power to take away their own power. But renouncing democracy is like a collective suicide -- or more precisely, like a rebirth: if someday society wishes to transform its foundations, it must be able to do so, but the process must be so difficult and deliberate that it only occurs when the consensus is genuine, sustained, and near-unanimous. That is why the protection mechanics must exist and be very strict.

The thresholds (95% legislative + 85% referendum + 75% census participation + 2 years of reflection + 21-year cooldown [one attempt per generation]) are not arbitrary: they seek to make the elimination of fundamental democratic guarantees extremely difficult, but not impossible. They were not devised with the intention of implanting a tyranny of old political systems over the living present; but as protection of future generations against irreversible decisions made under pressure or manipulation.

Of course, every measure justified as protection has the double edge of manipulation. Hence, from here I wish to encourage critical thinking about Level 6 consensus in the reader. I do not believe it is the perfect solution, but it is the best one I have come up with.

## Article 70: Mechanisms prevail over rights

Constitutional mechanisms (voting, revocation, separation of powers) are the ultimate guarantee of all rights. Without the democratic machine, rights lack effective protection.

That is why no right can be invoked to block the mechanisms: it would be using a piece of the machine to destroy the entire machine. It is like building a functional car but with a plastic body instead of metal: it works perfectly until the first crash, and then there is nothing to protect what is inside.

## Article 68: Ordinary reform and protection against bypass

Ordinary reform is the default mechanism for modifying any non-entrenched article: legislative N4 or popular N1 with 50% participation. It is deliberately accessible to allow the Constitution to evolve.

However, a potential loophole exists: if an article contains parameters protected at N5 or N6, a legislature with only N4 could reform the entire article, rewriting the parameters and bypassing their protection. To close this loophole, Article 68 establishes that the reform of an article requires consensus equal to or greater than the highest protection level of the parameters it contains. Thus, parameter protection cannot be circumvented through reform of the article that houses them.

The protection system is structured in three layers: entrenched clauses (Article 66) for irrenunciable fundamental principles, parameter protection (N3 to N6 depending on each article) for numerical values and specific configurations, and ordinary reform (Article 68) as the default mechanism for everything else.

---
---

# END OF PART 2
