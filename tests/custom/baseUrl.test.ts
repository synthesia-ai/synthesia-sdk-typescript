// Ours, kept from regeneration by .fernignore: a client built without baseUrl or environment sends
// requests to Synthesia's public API and nowhere else. If the spec's `servers` or our overrides change the generated
// default, this fails on the regeneration PR.
import { SynthesiaClient } from "../../src/index";

const BASE_URL = "https://developers.synthesia.io";

describe("default base URL", () => {
    it("sends requests to Synthesia's public API", async () => {
        const urls: string[] = [];
        const client = new SynthesiaClient({
            apiKey: "test",
            fetch: async (input) => {
                urls.push(input instanceof Request ? input.url : String(input));
                return Response.json({ data: [], nextCursor: null });
            },
        });

        await client.localizations.listLanguages();
        expect(urls).toEqual([`${BASE_URL}/api/localizations/languages`]);
    });
});
