"""Testes do kit: python3 -m unittest discover -s testes -v"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(RAIZ / "ferramentas"), str(RAIZ / "agentes")]

import clic_regras  # noqa: E402
import curio_triagem  # noqa: E402
import gancho_check  # noqa: E402
import link  # noqa: E402
import storyboard  # noqa: E402


def roteiro_bom():
    return {
        "id": "t", "idioma": "pt", "duracao": 15, "pergunta": "por que?",
        "gancho": {"texto": "Sua geladeira esquenta a sua cozinha.", "forma": "contrario", "imagem": "geladeira"},
        "reserva": [
            {"texto": "A sua geladeira tem um radiador nas costas.", "forma": "objeto", "imagem": "grade"},
            {"texto": "Trinta e cinco graus atrás da sua geladeira.", "forma": "numero", "imagem": "termômetro"},
            {"texto": "Já pôs a mão atrás da sua geladeira?", "forma": "pergunta", "imagem": "mão"},
        ],
        "fecho": "Manda para quem deixa a porta aberta.",
        "blocos": [
            {"id": "b0", "cena": "gancho", "frases": [{"id": "g", "texto": "Sua geladeira esquenta a sua cozinha.", "chave": "esquenta"}]},
            {"id": "b1", "cena": "grade", "frases": [{"id": "f1", "texto": "E não, não é a luz de dentro.", "chave": "luz"}]},
            {"id": "b2", "cena": "grade", "frases": [{"id": "f2", "texto": "Ela tira o calor da comida e joga pela grade.", "chave": "grade"}]},
            {"id": "b3", "cena": "fim", "frases": [{"id": "f3", "texto": "Manda para quem deixa a porta aberta.", "chave": "porta"}]},
        ],
        "cenas": {
            "gancho": {"que": "geladeira", "boceto": {"tipo": "objeto", "texto": "ESQUENTA"}},
            "grade": {"que": "grade vermelha", "boceto": {"tipo": "dentro", "texto": "calor"}},
            "fim": {"que": "celular", "boceto": {"tipo": "celular", "texto": "Enviar"}},
        },
    }


def pasta_com(r, fatos="# f\nhttps://exemplo.org\n", pie="Sua geladeira trabalha contra você.\n"):
    d = Path(tempfile.mkdtemp())
    (d / "roteiro.json").write_text(json.dumps(r, ensure_ascii=False))
    if fatos is not None:
        (d / "fatos.md").write_text(fatos)
    if pie is not None:
        (d / "pie.txt").write_text(pie)
    return d


class Gancho(unittest.TestCase):
    def test_roteiro_bom_passa(self):
        e, _ = gancho_check.checar(pasta_com(roteiro_bom()))
        self.assertEqual(e, [])

    def test_comecos_proibidos(self):
        for t in ["Em 1913, um engenheiro inventou a sua geladeira.", "Segundo um estudo, sua geladeira esquenta.",
                  "Hoje eu vou te explicar a geladeira.", "Você sabia que a geladeira esquenta?",
                  "Um dos maiores segredos da sua casa.", "Há 100 anos sua geladeira não existia."]:
            r = roteiro_bom()
            r["gancho"]["texto"] = t
            r["blocos"][0]["frases"][0]["texto"] = t
            e, _ = gancho_check.checar(pasta_com(r))
            self.assertTrue(any("gancho:" in x for x in e), t)

    def test_noticia_e_eu_reprovam(self):
        for t in ["A Samsung acaba de lançar sua geladeira nova.", "Eu descobri o segredo da sua geladeira."]:
            r = roteiro_bom()
            r["gancho"]["texto"] = t
            r["blocos"][0]["frases"][0]["texto"] = t
            e, _ = gancho_check.checar(pasta_com(r))
            self.assertTrue(any("gancho:" in x for x in e), t)

    def test_formas_repetidas(self):
        r = roteiro_bom()
        for x in r["reserva"]:
            x["forma"] = "contrario"
        e, _ = gancho_check.checar(pasta_com(r))
        self.assertTrue(any("repetem forma" in x for x in e))

    def test_numero_sem_fonte(self):
        r = roteiro_bom()
        r["blocos"][2]["frases"][0]["texto"] = "Atrás dela faz 35 graus."
        e, _ = gancho_check.checar(pasta_com(r))
        self.assertTrue(any("35" in x for x in e))
        e, _ = gancho_check.checar(pasta_com(r, fatos="35 graus · https://x.org\n"))
        self.assertFalse(any("35" in x for x in e))

    def test_fecho_cena_chave_pie(self):
        r = roteiro_bom()
        r["blocos"][3]["frases"][0]["texto"] = "Tchau."
        r["blocos"][1]["cena"] = "nao-existe"
        r["blocos"][2]["frases"][0]["chave"] = "banana"
        e, _ = gancho_check.checar(pasta_com(r, pie="#viral texto"))
        txt = " ".join(e)
        for trecho in ["fecho", "nao-existe", "banana", "hashtag"]:
            self.assertIn(trecho, txt)

    def test_duracao_longa(self):
        r = roteiro_bom()
        r["blocos"][2]["frases"][0]["texto"] = " ".join(["palavra"] * 80)
        e, _ = gancho_check.checar(pasta_com(r))
        self.assertTrue(any("passa muito" in x for x in e))

    def test_espanhol(self):
        r = roteiro_bom()
        r["idioma"] = "es"
        r["gancho"]["texto"] = "Según un estudio, tu nevera calienta."
        r["blocos"][0]["frases"][0]["texto"] = r["gancho"]["texto"]
        e, _ = gancho_check.checar(pasta_com(r))
        self.assertTrue(any("matiz" in x for x in e))


class Montar(unittest.TestCase):
    def test_chave_so_na_sua_frase(self):
        import re, subprocess
        r = roteiro_bom()
        r["blocos"][2]["frases"][0]["texto"] = "A luz esquenta? Ela tira o calor e joga pela grade."
        d = pasta_com(r)
        subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "montar.py"), "--projeto", str(d), "--sem-voz"],
                       check=True, capture_output=True)
        t = (d / "js" / "tempos.js").read_text()
        leg = json.loads(re.search(r"LEG = (\[.*?\]);\n", t).group(1))
        quentes = [q.lower() for g in leg for q in g["quente"]]
        self.assertEqual(quentes.count("esquenta"), 1)   # chave só da frase g
        self.assertIn("grade", quentes)


class Storyboard(unittest.TestCase):
    def test_gera_html(self):
        d = pasta_com(roteiro_bom())
        out, av = storyboard.gerar(d)
        h = out.read_text()
        self.assertIn("Storyboard", h)
        self.assertEqual(h.count('class="card"'), 3)  # 3 cenas, grade junta 2 blocos
        self.assertIn("<mark>esquenta</mark>", h)


class Clic(unittest.TestCase):
    def base(self, **kw):
        m = {"config": {"teto_dia": 150, "retorno_min": 1.5, "gasto_corte": 30}, "medicao_ok": True,
             "compradores_excluidos": True,
             "anuncios": [{"id": "A", "orcamento_dia": 30, "gasto": 60, "vendas": 4, "receita": 156},
                          {"id": "B", "orcamento_dia": 30, "gasto": 40, "vendas": 0, "receita": 0},
                          {"id": "C", "orcamento_dia": 30, "gasto": 10, "vendas": 0, "receita": 0}]}
        m.update(kw)
        return m

    def acoes(self, r):
        return {(p["acao"], p["anuncio"]) for p in r["propostas"]}

    def test_regras(self):
        r = clic_regras.propor(self.base())
        a = self.acoes(r)
        self.assertIn(("subir", "A"), a)      # retorno 2,6
        self.assertIn(("cortar", "B"), a)     # 40 sem venda
        self.assertIn(("trocar", "B"), a)
        self.assertIn(("manter", "C"), a)     # ainda aprendendo
        self.assertFalse(r["executa"])

    def test_teto(self):
        m = self.base()
        m["anuncios"] = [{"id": f"X{i}", "orcamento_dia": 45, "gasto": 90, "vendas": 5, "receita": 300} for i in range(3)]
        r = clic_regras.propor(m)
        self.assertLessEqual(r["orcamento_total_proposto"], 150.01)

    def test_sem_medicao_nada_sobe(self):
        r = clic_regras.propor(self.base(medicao_ok=False))
        self.assertNotIn(("subir", "A"), self.acoes(r))
        self.assertTrue(any("MEDIÇÃO" in x for x in r["alertas"]))

    def test_verba_espalhada_e_compradores(self):
        m = self.base(compradores_excluidos=False)
        m["anuncios"] = [{"id": f"P{i}", "orcamento_dia": 5, "gasto": 5, "vendas": 0, "receita": 0} for i in range(6)]
        r = clic_regras.propor(m)
        txt = " ".join(r["alertas"])
        self.assertIn("espalhada", txt)
        self.assertIn("compr", txt)

    def test_texto(self):
        self.assertIn("OK", clic_regras.texto(clic_regras.propor(self.base())))


class Curio(unittest.TestCase):
    def test_triagem(self):
        msgs = [{"id": "1", "de": "@ana", "texto": "Como você fez esse vídeo?"},
                {"id": "2", "de": "@bia", "texto": "quero reembolso"},
                {"id": "3", "de": "@marca", "texto": "Somos uma marca, topa parceria?"},
                {"id": "4", "de": "@c", "texto": "amei 😍"},
                {"id": "5", "de": "@d", "texto": "ok"}]
        r = curio_triagem.triar(msgs, "https://x.org/?utm_medium=dm")
        cls = {i["id"]: i["classe"] for i in r["itens"]}
        self.assertEqual(cls, {"1": "como_faz", "2": "reembolso", "3": "marca", "4": "elogio"})
        self.assertIn("https://x.org", r["itens"][0]["proposta"])
        self.assertFalse(r["envia"])
        r2 = curio_triagem.triar(msgs, "x", r["vistos"])
        self.assertFalse(r2["novidade"])
        self.assertEqual(curio_triagem.texto(r2), "Curio: nada novo.")


class Link(unittest.TestCase):
    def test_link(self):
        u = link.etiquetar("https://inema.club", "curiosidade", "reel", "geladeira")
        self.assertIn("utm_medium=reel", u)
        self.assertIn("utm_content=geladeira", u)
        with self.assertRaises(ValueError):
            link.etiquetar("https://inema.club", "c", "outro")


if __name__ == "__main__":
    unittest.main()
