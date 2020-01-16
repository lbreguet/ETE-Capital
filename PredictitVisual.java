import java.net.URL;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;

public class PredictitVisual {
	
	public static Document loadTestDocument(String url) throws Exception {
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		factory.setNamespaceAware(true);
		return factory.newDocumentBuilder().parse(new URL(url).openStream());
	}

	public static void main(String[] args) throws Exception {
		Document doc = loadTestDocument("https://www.predictit.org/api/marketdata/all");
		System.out.println(doc);
	}

}