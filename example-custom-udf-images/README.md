# TileDB Cloud configuration with custom UDF Images

This repository demonstrates configuring TileDB Cloud Enterprise Edition to use custom UDF images from user defined image repository.

## Background

TileDB Cloud Enterprise is configured by default to access Dockerhub UDF images. Images are built by TileDB to cover a large range of requirements for Geospatial, Genomics etc, and can be used as a base to create new custom images. Customers can use own Dockerhub repositories or AWS ECR.

## Requirements

- Configure TileDB Cloud Enterprise to access AWS ECR as an alternative to Dockerhub (default)
- Configure TileDB Cloud Enterprise to allow REST Server K8s service account to access ECR
- Create and upload custom images
- Configure TileDB Cloud Enterprise to use custom images
- Usage example

## Configuration


### AWS ECR Configuration

Replace `ContainerRegistry` key with following values to enable REST server access AWS ECR

```yaml
tiledb-cloud-rest:
  restConfig:
    ContainerRegistry:
      Host: "AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com"
      EnableDockerhubAuth: false
      EnableEcrAuth: true
```

### Enable REST Server K8s service account to access ECR

Provided that TileDB Enterprise Helm Chart is installed in namespace `tiledb-cloud`, the default service account of this namespace is used by REST Server. It has to be annotated as follows

```yaml
// default sa in tiledb-cloud namespace
Name: default
Namespace: tiledb-cloud
Annotations: eks.amazonaws.com/role-arn:arn:aws:iam::AWS_ACCOUNT_ID:role/tiledb-cloud-assume-role
```

This annotation refers to an AWS Role, that has to include a policy statement to allow ECR access:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ECRReadOnly",
            "Effect": "Allow",
            "Action": [
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetAuthorizationToken",
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability"
            ],
            "Resource": "*"
        },
     ...
    ]
}
```

### Create and upload custom images

We will use existing images from TileDB Inc. as base to create new custom images

#### Login and download generic image from Dockerhub

```bash
docker login -u username
docker pull docker.io/tiledbenterprise/rest-python-udf-3.9:2.23.4
```

#### Build custom image

Create a new Dockerfile

```bash
vi Dockerfile-rest-python-udf-custom
```

Use `tiledbenterprise/rest-python-udf-3.9:2.23.4` as base and install a package that does not exist in stock image 

```Dockerfile
FROM tiledbenterprise/rest-python-udf-3.9:2.23.4

USER root
WORKDIR /tmp

# mamba install custom packages
RUN mamba install -c conda-forge pillow

USER udf
WORKDIR /home/udf
```

Build image

```bash
docker buildx build -t AWS_ACCOUT_ID.dkr.ecr.AWS_REGION.amazonaws.com/tiledbenterprise/rest-python-udf-custom-3.9:2.23.4 -f Dockerfile-rest-python-udf-custom .
```

Login to AWS ECR and push new image

```bash
docker push AWS_ACCOUT_ID.dkr.ecr.AWS_REGION.amazonaws.com/tiledbenterprise/rest-python-udf-custom-3.9:2.23.4
```

#### Configure TileDB Cloud Enterprise to use custom images

In the following example, we add a new entry for our custom image under section `CustomeImages`, version 3.8, 3.9:

```yaml
"my_custom_image": "tiledbenterprise/rest-python-udf-custom-3.9:2.23.4" 
```

This is the same image we uploaded earlier to ECR

```yaml
tiledb-cloud-rest:
  restConfig:
    UDF:
      Images:
        # Make sure tiledb-rest.yaml.example and chart/tiledb-cloud-rest/values.yaml
        # stay in sync with each other.
        "python":
          # Python UDFs must be run with a version compatible with the one that
          # serialized ("pickled") the function, so images must be available
          # for all Python client versions you want to support.
          - Versions: ["", "3.6", "3.7"]
            #   # Old TileDB-Cloud-Py clients didn't send language version,
            #   # so we use py3.7 with them ("" means this will be chosen
            #   # if no version is specified).  Python 3.6 and 3.7 are compatible.
            #   # Starting from images 2.20.2 support for Python 3.7 is deprecated
            DefaultImage: "tiledbenterprise/rest-python-udf:2.19.7"
            CustomImages:
              "genomics": "tiledbenterprise/rest-python-udf-gen-3.7:2.19.7"
              "geo": "tiledbenterprise/rest-python-udf-geo:2.19.7"
              "imaging-dev": "tiledbenterprise/rest-python-udf-imaging-3.7:2.19.7"
          - Versions: ["3.8", "3.9"] # mutually function-pickle–compatible
            DefaultImage: "tiledbenterprise/rest-python-udf-3.9:2.23.4"
            CustomImages:
              "genomics": "tiledbenterprise/rest-python-udf-gen:2.23.4"
              "geo": "tiledbenterprise/rest-python-udf-geo-3.9:2.23.4"
              "imaging-dev": "tiledbenterprise/rest-python-udf-imaging:2.23.4"
              "vectorsearch": "tiledbenterprise/rest-python-udf-vectorsearch:2.23.4"
              "my_custom_image": "tiledbenterprise/rest-python-udf-custom-3.9:2.23.4"   
        "r":
          # R is largely compatible across versions.
          # "*" denotes a fallback, i.e., it will be used for *any* version
          # not present in other ImageSets (which in this case is all versions).
          - Versions: ["*"]
            DefaultImage: "tiledbenterprise/rest-r-udf:2.23.4"
```

## Usage

Every section under Images, includes a `Version` array entry. Images that are included under `Default` or `CustomImages` fields are enabled based on the client environment. For our example we need to use 3.9 images, as a result we are creating an environment for Python 3.9 using conda:

```bash
conda create --name custom_image python=3.9
```

Then install dependencies

```bash
pip install .
```

Then run `python custom_image.py`. The, will use 3.9 section of images because the client uses 3.9, while `image_name` argument will select the correct custom image. Please note that if no image is defined, the default is used. The result can be seen under `Monitor->Logs Tasks` section in TileDB Cloud Console, showing that owr custom images= using the additional package is used:

```bash
[2024-07-09 20:24:16,867] [custom] [test_custom_image] [INFO] (209, 123, 193)
[2024-07-09 20:24:16,867] [custom] [test_custom_image] [INFO] 0.29.0
[2024-07-09 20:24:16,867] [custom] [test_custom_image] [INFO] (2, 23, 1)
```

## Custom Images using Python 3.11

We will provide an example of how to build a Dockerfile for Python 3.11 soon

References
1. [Custom User Defined Images](https://app.gitbook.com/o/-LnZGqrmM4XMrJx6aqI-/s/-MZPCnMe65GdoyPLaTdA/custom-user-defined-images)
2. [Configure AWS ECR Container Registry for UDF Images](https://app.gitbook.com/o/-LnZGqrmM4XMrJx6aqI-/s/-MZPCnMe65GdoyPLaTdA/custom-user-defined-images/configure-aws-ecr-container-registry-for-udf-images)