from genebe.vcf_simple_annotator import annotate_vcf

# annotate_vcf(
#     "/tmp/gb/x_split.vcf",
#     "/tmp/gb/output.vcf",
#     genome="hg19",
#     batch_size=50,
#     endpoint_url="https://api.genebe.net/cloud/api-public/v1/variants",
# )

annotate_vcf(
    "/tmp/gb/x_split.vcf",
    "/tmp/gb/output.vcf",
    genome="hg19",
    batch_size=1000,
    endpoint_url="http://localhost:7180/cloud/api-public/v1/variants",
)
