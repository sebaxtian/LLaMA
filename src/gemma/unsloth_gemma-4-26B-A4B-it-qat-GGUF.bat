:: ==============================================================================
:: LÍNEA BASE DE PRODUCCIÓN: PERFIL RENDIMIENTO MÁXIMO
:: Modelo: Gemma-4-26B-A4B-it-qat-GGUF (UD-Q4_K_XL)
:: Hardware: NVIDIA GeForce RTX 5060 Ti 16GB (CUDA 13.5) + Intel i9-13900H + 32 GB RAM
:: Sistema operativo: Windows 11
:: Parámetros destacados: -ncmoe 9 | --ubatch-size 1120 | --spec-draft-n-max 3
:: ==============================================================================
..\..\bin\llama-master-bin-win-rtx5060ti-cuda-13.5-x64\llama-server.exe ^
  --model ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf ^
  --mmproj ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\mmproj-BF16.gguf ^
  --model-draft ..\..\models\gemma\unsloth_gemma-4-26B-A4B-it-qat-GGUF\mtp-gemma-4-26B-A4B-it-Q4_0.gguf ^
  --spec-type draft-mtp ^
  --spec-draft-n-max 3 ^
  --flash-attn on ^
  --ubatch-size 1120 ^
  --gpu-layers all ^
  --fit off ^
  -ncmoe 9 ^
  --cache-idle-slots ^
  --reasoning on ^
  --ctx-size 131072 ^
  --temp 1.0 ^
  --top-p 0.95 ^
  --top-k 64 ^
  --parallel 1 ^
  --log-verbosity 4 ^
  --cache-type-k q8_0 ^
  --cache-type-v q8_0 ^
  --cache-type-k-draft q8_0 ^
  --cache-type-v-draft q8_0 ^
  --alias Gemma-4-26B-A4B
