# Bayesian Color Constancy via Physics-Based Inverse Rendering
*Jinnie Sun*

A Bayesian model of color constancy that inverts a physically based renderer ([Mitsuba 3](https://mitsuba-renderer.org)) to infer **object chromaticity**, **illuminant chromaticity**, and **surface glossiness** from a single image — and asks whether specular highlights actually help.

> Course project, Yale University, Algorithms of the Mind, Fall 2025 · [Report (PDF)](final_report_js4872.pdf)


## Motivation

The light reaching the eye is a product of surface reflectance and illumination, so recovering an object's color is an ill-posed inverse problem. Psychophysics suggests specular highlights help humans disambiguate the two. This project tests that idea computationally with an analysis-by-synthesis model.

## Method

**Generative model.** Latent parameters θ = (u′<sub>O</sub>, v′<sub>O</sub>, u′<sub>L</sub>, v′<sub>L</sub>, α) — object and illuminant chromaticity in CIE u′v′, plus specular roughness α — are mapped to linear RGB and rendered in a fixed 3D scene (central sphere, Mondrian back wall, directional light). Uniform prior; Gaussian pixel likelihood.

**Hybrid inference.** Rendering every MCMC proposal is expensive, so inference is two-stage:
1. **Amortized initialization** — an MLP trained on 1,000 prior-sampled image–parameter pairs gives a point estimate.
2. **MCMC refinement** — Random-Walk Metropolis–Hastings with truncated-normal proposals refines the estimate and quantifies posterior uncertainty.

**Design.** 5 object × 5 illuminant chromaticities × 2 materials (matte α = 0.99, glossy α = 0.01), 8 runs each → 400 runs. Error = Euclidean distance in u′v′ between posterior mean and ground truth.

## Key Results

- **Accurate recovery overall**, better along the red–green axis than yellow–blue (object u′ r = 0.84 vs. v′ r = 0.68).
- **Specularity is a trade-off, not a free cue:** glossiness slightly improves object color recovery (p = 0.09) but impairs illuminant estimation (p = 0.04). Sparse, high-frequency highlights make the pixel-wise likelihood brittle.
- **Chromatic bias opposite to humans:** the model is most accurate under red light and worst under blue, whereas human constancy is strongest along the daylight locus — consistent with humans relying on a daylight prior that this uniform-prior model lacks.
