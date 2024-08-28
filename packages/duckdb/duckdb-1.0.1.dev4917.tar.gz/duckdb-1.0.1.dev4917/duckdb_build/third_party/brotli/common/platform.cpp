/* Copyright 2016 Google Inc. All Rights Reserved.

   Distributed under MIT license.
   See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
*/

#include <stdlib.h>

#include <brotli/types.h>

#include "brotli_platform.h"


/* Default brotli_alloc_func */
void*  duckdb_brotli::BrotliDefaultAllocFunc(void* opaque, size_t size) {
  BROTLI_UNUSED(opaque);
  return malloc(size);
}

/* Default brotli_free_func */
void  duckdb_brotli::BrotliDefaultFreeFunc(void* opaque, void* address) {
  BROTLI_UNUSED(opaque);
  free(address);
}
