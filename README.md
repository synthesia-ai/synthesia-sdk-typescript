# Synthesia TypeScript Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Fsynthesia-ai%2Fsynthesia-sdk-typescript)
[![npm shield](https://img.shields.io/npm/v/@synthesia-ai/sdk)](https://www.npmjs.com/package/@synthesia-ai/sdk)

This SDK is under active development and is not yet fully stable. Its interface may change in any release before 1.0. Breaking changes bump the minor version.

## Table of Contents

- [Documentation](#documentation)
- [Installation](#installation)
- [Reference](#reference)
- [Keep Your Api Key on The Server](#keep-your-api-key-on-the-server)
- [Timeouts](#timeouts)
- [Retries](#retries)
- [Verify A Release](#verify-a-release)
- [Support](#support)
- [Usage](#usage)
- [Environments](#environments)
- [Request and Response Types](#request-and-response-types)
- [Exception Handling](#exception-handling)
- [Pagination](#pagination)
- [Advanced](#advanced)
  - [Subpackage Exports](#subpackage-exports)
  - [Additional Headers](#additional-headers)
  - [Additional Query String Parameters](#additional-query-string-parameters)
  - [Aborting Requests](#aborting-requests)
  - [Access Raw Response Data](#access-raw-response-data)
  - [Logging](#logging)
  - [Custom Fetch](#custom-fetch)
  - [Runtime Compatibility](#runtime-compatibility)

## Documentation

API reference documentation is available [here](https://developers.synthesia.io/docs/introduction).

## Installation

```sh
npm i -s @synthesia-ai/sdk
```

## Reference

A full reference for this library is available [here](https://github.com/synthesia-ai/synthesia-sdk-typescript/blob/HEAD/./reference.md).

## Keep your API key on the server

Use this SDK only in server-side code, and never put your API key in code you ship to users. Without an `apiKey` option, the client reads the key from the `SYNTHESIA_API_KEY` environment variable:

```typescript
import { SynthesiaClient } from "@synthesia-ai/sdk";

const client = new SynthesiaClient(); // Uses SYNTHESIA_API_KEY
```


## Timeouts

The SDK defaults to a 90 second timeout. Use the `timeoutInSeconds` option to configure this behavior.

```typescript
const response = await client.localizations.get(..., {
    timeoutInSeconds: 30 // override timeout to 30s
});
```


## Retries

The SDK retries a failed request up to 2 times, with exponential backoff, when the response status is 408, 429 or 5XX. It waits as long as a `Retry-After` header asks, up to 60 seconds.

Requests that create something (an interactive avatar, a session or a localization) are never retried, so a timeout can't create a duplicate. Check whether the first request succeeded before you send it again.

Use the `maxRetries` option to change the number of retries for other requests:

```typescript
const response = await client.localizations.get(..., {
    maxRetries: 0 // override maxRetries at the request level
});
```

## Verify a release

Every release is published from this repository's release workflow with [npm provenance](https://docs.npmjs.com/generating-provenance-statements), which links the package to the commit and workflow run that built it. To check the signatures and provenance of the packages you've installed, run this in your project:

```sh
npm audit signatures
```

The package page on npmjs.com also shows the provenance under "Provenance".


## Support

For help with the SDK or the API, see the [API documentation](https://developers.synthesia.io/docs/introduction) or [contact Synthesia Support](https://help.synthesia.io/en/articles/7182166-how-can-i-contact-synthesia). To report a security issue, follow [SECURITY.md](./SECURITY.md).

This SDK is generated from the Synthesia API definition, so we don't accept pull requests to this repository.

## Usage

Instantiate and use the client with the following:

```typescript
import { SynthesiaClient } from "@synthesia-ai/sdk";

const client = new SynthesiaClient({ apiKey: "YOUR_API_KEY" });
await client.localizations.createFromMediaUrl({
    lipsyncEnabled: true,
    burnedInCaptionsEnabled: false,
    mediaUrl: "https://my-bucket.s3.amazonaws.com/onboarding.mp4?X-Amz-Signature=...",
    title: "Product onboarding",
    sourceLanguage: "en-US",
    targetLanguages: ["es-ES", "fr-FR"]
});
```

## Environments

This SDK allows you to configure different environments for API requests.

```typescript
import { SynthesiaClient, SynthesiaEnvironment } from "@synthesia-ai/sdk";

const client = new SynthesiaClient({
    environment: SynthesiaEnvironment.Default,
});
```

## Request and Response Types

The SDK exports all request and response types as TypeScript interfaces. Simply import them with the
following namespace:

```typescript
import { Synthesia } from "@synthesia-ai/sdk";

const request: Synthesia.ListLanguagesRequest = {
    ...
};
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```typescript
import { SynthesiaError } from "@synthesia-ai/sdk";

try {
    await client.localizations.createFromMediaUrl(...);
} catch (err) {
    if (err instanceof SynthesiaError) {
        console.log(err.statusCode);
        console.log(err.message);
        console.log(err.body);
        console.log(err.rawResponse);
    }
}
```

## Pagination

List endpoints are paginated. The SDK provides an iterator so that you can simply loop over the items:

```typescript
import { SynthesiaClient } from "@synthesia-ai/sdk";

const client = new SynthesiaClient({ apiKey: "YOUR_API_KEY" });
const pageableResponse = await client.localizations.listLanguages();
for await (const item of pageableResponse) {
    console.log(item);
}

// Or you can manually iterate page-by-page
let page = await client.localizations.listLanguages();
while (page.hasNextPage()) {
    page = await page.getNextPage();
}

// You can also access the underlying response
const response = page.response;
```

## Advanced

### Subpackage Exports

This SDK supports direct imports of subpackage clients, which allows JavaScript bundlers to tree-shake and include only the imported subpackage code. This results in much smaller bundle sizes.

```typescript
import { BillingClient } from '@synthesia-ai/sdk/billing';

const client = new BillingClient({...});
```

### Additional Headers

If you would like to send additional headers as part of the request, use the `headers` request option.

```typescript
import { SynthesiaClient } from "@synthesia-ai/sdk";

const client = new SynthesiaClient({
    ...
    headers: {
        'X-Custom-Header': 'custom value'
    }
});

const response = await client.localizations.createFromMediaUrl(..., {
    headers: {
        'X-Custom-Header': 'custom value'
    }
});
```

### Additional Query String Parameters

If you would like to send additional query string parameters as part of the request, use the `queryParams` request option.

```typescript
const response = await client.localizations.createFromMediaUrl(..., {
    queryParams: {
        'customQueryParamKey': 'custom query param value'
    }
});
```

### Aborting Requests

The SDK allows users to abort requests at any point by passing in an abort signal.

```typescript
const controller = new AbortController();
const response = await client.localizations.createFromMediaUrl(..., {
    abortSignal: controller.signal
});
controller.abort(); // aborts the request
```

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.withRawResponse()` method.
The `.withRawResponse()` method returns a promise that results to an object with a `data` and a `rawResponse` property.

```typescript
const { data, rawResponse } = await client.localizations.createFromMediaUrl(...).withRawResponse();

console.log(data);
console.log(rawResponse.headers['X-My-Header']);
```

### Logging

The SDK supports logging. You can configure the logger by passing in a `logging` object to the client options.

```typescript
import { SynthesiaClient, logging } from "@synthesia-ai/sdk";

const client = new SynthesiaClient({
    ...
    logging: {
        level: logging.LogLevel.Debug, // defaults to logging.LogLevel.Info
        logger: new logging.ConsoleLogger(), // defaults to ConsoleLogger
        silent: false, // defaults to true, set to false to enable logging
    }
});
```
The `logging` object can have the following properties:
- `level`: The log level to use. Defaults to `logging.LogLevel.Info`.
- `logger`: The logger to use. Defaults to a `logging.ConsoleLogger`.
- `silent`: Whether to silence the logger. Defaults to `true`.

The `level` property can be one of the following values:
- `logging.LogLevel.Debug`
- `logging.LogLevel.Info`
- `logging.LogLevel.Warn`
- `logging.LogLevel.Error`

To provide a custom logger, you can pass in an object that implements the `logging.ILogger` interface.

<details>
<summary>Custom logger examples</summary>

Here's an example using the popular `winston` logging library.
```ts
import winston from 'winston';

const winstonLogger = winston.createLogger({...});

const logger: logging.ILogger = {
    debug: (msg, ...args) => winstonLogger.debug(msg, ...args),
    info: (msg, ...args) => winstonLogger.info(msg, ...args),
    warn: (msg, ...args) => winstonLogger.warn(msg, ...args),
    error: (msg, ...args) => winstonLogger.error(msg, ...args),
};
```

Here's an example using the popular `pino` logging library.

```ts
import pino from 'pino';

const pinoLogger = pino({...});

const logger: logging.ILogger = {
  debug: (msg, ...args) => pinoLogger.debug(args, msg),
  info: (msg, ...args) => pinoLogger.info(args, msg),
  warn: (msg, ...args) => pinoLogger.warn(args, msg),
  error: (msg, ...args) => pinoLogger.error(args, msg),
};
```
</details>


### Custom Fetch

The SDK provides a low-level `fetch` method for making custom HTTP requests while still
benefiting from SDK-level configuration like authentication, retries, timeouts, and logging.
This is useful for calling API endpoints not yet supported in the SDK.

```typescript
const response = await client.fetch("/v1/custom/endpoint", {
    method: "GET",
}, {
    timeoutInSeconds: 30,
    maxRetries: 3,
    headers: {
        "X-Custom-Header": "custom-value",
    },
});

const data = await response.json();
```

### Runtime Compatibility


The SDK works in the following runtimes:



- Node.js 18+
- Vercel
- Cloudflare Workers
- Deno v1.25+
- Bun 1.0+
- React Native
