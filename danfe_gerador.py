from brazilfiscalreport.danfe import Danfe
from pathlib import Path
from typing import Optional

class DANFEPersonalizado:
    """Classe para gerar DANFE com layout personalizado."""

    def __init__(
        self,
        logo_path: str = None,
        empresa_nome: str = None,
        cores_personalizadas: dict = None,
        margens: dict = None,
    ):
        """
        Inicializa gerador DANFE personalizado.

        Args:
            logo_path: Caminho da logo da empresa
            empresa_nome: Nome da empresa
            cores_personalizadas: Dicionário com cores RGB
            margens: Dicionário com margens (top, right, bottom, left)
        """
        self.logo_path = logo_path
        self.empresa_nome = empresa_nome
        self.cores = cores_personalizadas or {}
        self.margens = margens or {
            'top': 10,
            'right': 10,
            'bottom': 10,
            'left': 10
        }

    def validar_logo(self) -> bool:
        """Valida se logo existe e é um arquivo válido."""
        if not self.logo_path:
            return False

        logo_file = Path(self.logo_path)
        if not logo_file.exists():
            print(f"✗ Logo não encontrada: {self.logo_path}")
            return False

        # Verificar extensão
        extensoes_validas = {'.png', '.jpg', '.jpeg', '.bmp'}
        if logo_file.suffix.lower() not in extensoes_validas:
            print(f"✗ Formato de logo inválido: {logo_file.suffix}")
            return False

        # Verificar tamanho (máx 500KB)
        tamanho_mb = logo_file.stat().st_size / (1024 * 1024)
        if tamanho_mb > 0.5:
            print(f"✗ Logo muito grande: {tamanho_mb:.2f}MB (máx 0.5MB)")
            return False

        print(f"✓ Logo validada: {self.logo_path}")
        return True

    def gerar_danfe(
        self,
        xml_path: str,
        output_path: Optional[str] = None
    ) -> bool:
        """
        Gera DANFE com customizações.

        Args:
            xml_path: Caminho do XML
            output_path: Caminho de saída (opcional)

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Ler XML
            xml_file = Path(xml_path)
            if not xml_file.exists():
                print(f"✗ XML não encontrado: {xml_path}")
                return False

            xml_content = xml_file.read_text(encoding='utf-8')
            print(f"✓ XML lido: {xml_file.name}")

            # Validar logo se configurada
            if self.logo_path and not self.validar_logo():
                print("⚠ Gerando DANFE sem logo")
                self.logo_path = None

            # Configurar margens
            margins_config = None
            if self.margens:
                from brazilfiscalreport.danfe.config import Margins
                margins_config = Margins(
                    top=self.margens.get('top', 5),
                    right=self.margens.get('right', 5),
                    bottom=self.margens.get('bottom', 5),
                    left=self.margens.get('left', 5)
                )

            # Configurar DANFE
            from brazilfiscalreport.danfe.config import DanfeConfig

            danfe_config = DanfeConfig(
                logo=self.logo_path,
                margins=margins_config if margins_config else Margins()
            )

            danfe = Danfe(xml_content, config=danfe_config)

            # Definir output
            if output_path is None:
                output_path = xml_file.with_suffix('.pdf')
            else:
                output_path = Path(output_path)

            # Gerar PDF
            danfe.output(str(output_path))

            tamanho_kb = output_path.stat().st_size / 1024
            print(f"✓ DANFE gerada: {output_path}")
            print(f"✓ Tamanho: {tamanho_kb:.2f} KB")

            return True

        except Exception as e:
            print(f"✗ Erro ao gerar DANFE: {e}")
            import traceback
            traceback.print_exc()
            return False

    def gerar_lote(
        self,
        pasta_xml: str,
        pasta_saida: Optional[str] = None
    ) -> dict:
        """
        Gera DANFE em lote para múltiplos XMLs.

        Args:
            pasta_xml: Pasta contendo XMLs
            pasta_saida: Pasta de saída (opcional)

        Returns:
            Dicionário com estatísticas
        """
        pasta_xml = Path(pasta_xml)
        pasta_saida = Path(pasta_saida or pasta_xml)
        pasta_saida.mkdir(parents=True, exist_ok=True)

        stats = {
            'total': 0,
            'sucesso': 0,
            'erro': 0,
            'arquivos': []
        }

        print(f"\n📦 Processando XMLs de {pasta_xml}")
        print("=" * 60)

        for xml_file in pasta_xml.glob('*.xml'):
            stats['total'] += 1

            output_file = pasta_saida / xml_file.stem

            print(f"\n[{stats['total']}] {xml_file.name}")

            if self.gerar_danfe(str(xml_file), str(output_file)):
                stats['sucesso'] += 1
                stats['arquivos'].append({
                    'xml': xml_file.name,
                    'pdf': output_file.name,
                    'status': 'sucesso'
                })
            else:
                stats['erro'] += 1
                stats['arquivos'].append({
                    'xml': xml_file.name,
                    'status': 'erro'
                })

        # Resumo
        print("\n" + "=" * 60)
        print(f"📊 RESUMO:")
        print(f"   Total:   {stats['total']}")
        print(f"   Sucesso: {stats['sucesso']} ✓")
        print(f"   Erro:    {stats['erro']} ✗")
        print("=" * 60)

        return stats
