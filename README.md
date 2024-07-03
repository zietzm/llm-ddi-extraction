# Drug-drug interactions extraction

How well can GPT-4 extract drugs/ingredients from the `DI` (drug interaction) section of drug labels?

We provided these to GPT-4 and evaluated performance using 100 labels that were manually annotated by two labelers (Michael and Undina).
The two sets of manual annotations were merged by hand, re-consulting the labels to ensure that nothing was missed or falsely included.

The evaluation was done two ways.
First, we evaluated how well the GPT annotations matched the manual annotations using a direct semantic similarity.
Any GPT annotation with an `llmrails/ember-v1` cosine similarity greater than a cutoff (0.7097613) was considered a match.
We evaluated the precision (fraction of GPT annotations that matched a manual annotation) and recall (fraction of manual annotations that were matched by GPT) on a per-label basis.
We found precision of 98.9% (721/729) and recall of 0.732 (827/1130).

Second, we mapped both GPT and manual annotations to RxNorm ingredients and evaluated how reliably the two methods selected the same RxNorm concepts.
To match annotations to RxNorm concepts, we used the same embedding and cosine similarity method, but this time with a more stringent cutoff (0.9), based on an inspection of the matches for manual annotations.
Below 0.9, the matches were not clearly related, whereas, above, they all appeared to be correct.
We evaluated the precision (fraction of GPT mapped RxNorm ingredients that were the same as the manual mapped RxNorm ingredient) and recall (fraction of manual mapped RxNorm ingredients that were identified by GPT after mapping to RxNorm).
We found precision of 92.8% (399/430) and recall of 59.2% (399/674).

For questions, contact Michael Zietz (@zietzm).
