# Reference
## billing
<details><summary><code>client.billing.<a href="/src/api/resources/billing/client/Client.ts">getCredits</a>() -> Synthesia.Credits</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get your workspace's current billing period and its credit balance.

Amounts are decimal strings (e.g. `"288.00"`).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```typescript
await client.billing.getCredits();

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**requestOptions:** `BillingClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Localizations
<details><summary><code>client.localizations.<a href="/src/api/resources/localizations/client/Client.ts">listLanguages</a>({ ...params }) -> core.Page&lt;Synthesia.Language, Synthesia.PageLanguage&gt;</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List the languages you can localize from and into, with the roles each supports.

**Required scope:** [`localization:read`](https://developers.synthesia.io/docs/scopes) (in Studio: Localization (read))
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```typescript
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
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `Synthesia.ListLanguagesRequest` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `LocalizationsClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.localizations.<a href="/src/api/resources/localizations/client/Client.ts">get</a>({ ...params }) -> Synthesia.Localization</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Required scope:** [`localization:read`](https://developers.synthesia.io/docs/scopes) (in Studio: Localization (read))
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```typescript
await client.localizations.get({
    localization_id: "localization_id"
});

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `Synthesia.GetLocalizationRequest` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `LocalizationsClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.localizations.<a href="/src/api/resources/localizations/client/Client.ts">createFromMediaUrl</a>({ ...params }) -> Synthesia.Localization</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Start localizing a video from a URL.

Poll `GET /localizations/{localization_id}` until `done` is true, then poll its locales until each is done.

**Required scope:** [`localization:write`](https://developers.synthesia.io/docs/scopes) (in Studio: Localization (write))
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```typescript
await client.localizations.createFromMediaUrl({
    lipsyncEnabled: true,
    burnedInCaptionsEnabled: false,
    mediaUrl: "https://my-bucket.s3.amazonaws.com/onboarding.mp4?X-Amz-Signature=...",
    title: "Product onboarding",
    sourceLanguage: "en-US",
    targetLanguages: ["es-ES", "fr-FR"]
});

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `Synthesia.CreateLocalizationFromMediaUrl` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `LocalizationsClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## InteractiveAvatars Sessions
<details><summary><code>client.interactiveAvatars.sessions.<a href="/src/api/resources/interactiveAvatars/resources/sessions/client/Client.ts">create</a>({ ...params }) -> Synthesia.Session</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Start an interactive avatar session.

- Each running session counts toward your plan's concurrent-session limit until it ends.
- Only sessions started through this API count toward the limit.
- Over the limit, the request fails with `429` and code `concurrency_limit`; its `detail`
  states your plan's limit and how many sessions are running.

| Plan | Concurrent sessions |
| --- | --- |
| Freemium | 1 |
| All paid plans | 100 |

**Required scope:** [`interactive_avatars:write`](https://developers.synthesia.io/docs/scopes) (in Studio: Interactive Avatars (write))
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```typescript
await client.interactiveAvatars.sessions.create({
    avatarIds: ["av_6c9edb85a2f947e5"],
    livekitUrl: "wss://your-app.livekit.cloud",
    livekitToken: "<your-livekit-token>"
});

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `Synthesia.interactiveAvatars.NewSession` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `SessionsClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## InteractiveAvatars Avatars
<details><summary><code>client.interactiveAvatars.avatars.<a href="/src/api/resources/interactiveAvatars/resources/avatars/client/Client.ts">create</a>({ ...params }) -> Synthesia.InteractiveAvatar</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create an interactive avatar from an existing Studio avatar.

- Generation is asynchronous: the request answers `202` with the avatar's current status.
- Poll by repeating the same request (with `regenerate` omitted) until `done` is true — a
  repeat never starts a second generation.
- Each poll re-runs the credit check, so a drained balance answers `402` even while an
  already-dispatched generation continues.
- Once `status` is `completed`, include the returned `id` in the `avatarIds` list of
  `POST /api/interactive-avatars/sessions`.

**Required scope:** [`interactive_avatars:write`](https://developers.synthesia.io/docs/scopes) (in Studio: Interactive Avatars (write))
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```typescript
await client.interactiveAvatars.avatars.create({
    sourceId: "av_6c9edb85a2f947e5",
    regenerate: false
});

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `Synthesia.interactiveAvatars.NewInteractiveAvatar` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `AvatarsClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Localizations Locales
<details><summary><code>client.localizations.locales.<a href="/src/api/resources/localizations/resources/locales/client/Client.ts">list</a>({ ...params }) -> core.Page&lt;Synthesia.Locale, Synthesia.PageLocale&gt;</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Required scope:** [`localization:read`](https://developers.synthesia.io/docs/scopes) (in Studio: Localization (read))
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```typescript
const pageableResponse = await client.localizations.locales.list({
    localization_id: "localization_id"
});
for await (const item of pageableResponse) {
    console.log(item);
}

// Or you can manually iterate page-by-page
let page = await client.localizations.locales.list({
    localization_id: "localization_id"
});
while (page.hasNextPage()) {
    page = await page.getNextPage();
}

// You can also access the underlying response
const response = page.response;

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `Synthesia.localizations.ListLocalesRequest` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `LocalesClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.localizations.locales.<a href="/src/api/resources/localizations/resources/locales/client/Client.ts">add</a>({ ...params }) -> Synthesia.PageLocale</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add a locale for each language, and return the requested locales.

- 202 when new locales were added: poll them until each is done.
- 200 when every language already had a locale.
- A language that already has a locale is skipped, so repeating a request is safe. A failed locale isn't
  redone: create a new localization to retry it.
- Locales are never removed: a language left out keeps its locale.

**Required scope:** [`localization:write`](https://developers.synthesia.io/docs/scopes) (in Studio: Localization (write))
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```typescript
await client.localizations.locales.add({
    localization_id: "localization_id",
    lipsyncEnabled: true,
    burnedInCaptionsEnabled: false,
    locales: [{
            language: "es-ES",
            generate: true
        }]
});

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `Synthesia.localizations.AddLocales` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `LocalesClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

