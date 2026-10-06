import { describe, expect, it } from "vitest";
import viteConfig from "../../vite.config";
import { buildPatientsUrl } from "./api";

describe("serviço de pacientes", () => {
  it("respeita o caminho base do portal publicado no GitHub Pages", () => {
    expect(viteConfig.base).toBe("/grupo-aura-cardioia-portal/");
    expect(buildPatientsUrl(viteConfig.base)).toBe(
      "/grupo-aura-cardioia-portal/data/patients.json",
    );
  });
});
