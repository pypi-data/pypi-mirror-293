# AuroraCap



Video Detailed Captioning is a key task which aims to generate compre-
hensive and coherent textual descriptions of video content, benefiting both
video understanding and generation. 

We propose AuroraCap, a simple video
caption baseline based on a large vision-language model. We follow the
simplest architecture, similar to LLaVA, without additional parameters
for temporal modeling. To address the overhead caused by lengthy video
sequences, we implemented a token merging strategy, reducing the num-
ber of visual tokens input to the LLM to just 1% of the original amount.
Surprisingly, we found that this strategy results in almost no performance
drop. AuroraCap shows advancing performance on various video and
image captioning benchmarks compared to existing models.

You can use
[AuroraCap](https://huggingface.co/Reself/AuroraCap-7B-VID)
to download our model.