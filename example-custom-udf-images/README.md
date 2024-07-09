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

## Usage
