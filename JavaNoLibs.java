import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.URI;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.net.URL;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.time.Duration;
import java.time.Instant;

public class Nasa
{
    private static int max = 0, average = 0;
    private static String result = "";
    
    public static void main(String[] args) throws Exception
    {
        for (int i = 0; i <5; i++)
        {
            // starting the timer to record the performance time
            Instant start = Instant.now();
            
            // creating instance of client for further connection
            HttpClient client = HttpClient.newHttpClient();
            
            // using builder pattern to create a get request to NASA API url
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=DEMO_KEY"))
                    .build();
                    
            // sending get request to the API url
            HttpResponse <String> response = client.send(request, BodyHandlers.ofString());
            
            // retrieving the body of response, which is going to be a string representation of JSON object, provided by server
            String raw = response.body();
            
            // modifying the received string for easier analysis
            raw = raw.replace("JPG", "jpg");
            raw = raw.replace ("PNG", "png");
            
            while (raw.indexOf("http") != -1)
            {
                int beg = raw.indexOf(":\"http");
                int end = raw.indexOf(".jpg");
                
                if (end > raw.indexOf(".png") && raw.indexOf(".png") != -1)
                {
                    end = raw.indexOf(".png");
                }
                
                if (end == -1)
                {
                    end = raw.indexOf(".png");
                }
                
                // extract and prepare a link to be passed as an image location
                String rawLink = raw.substring(beg+2, end+4);
                raw = raw.substring(end + 4);
                String cleanLink = rawLink.replace("http", "https").replace(".jpl", "");
                
                analyseSizeOfImage(cleanLink);
            }
            
            // display the time and results
            /* Instant end = Instant.now();
            System.out.println(max + " -- " + result);
            System.out.println(Duration.between(start,end).toMillis());*/
            
            Instant end = Instant.now();
            average += Duration.between(start,end).toMillis();
        }
        System.out.println(result);
        System.out.println(average/5);
    }
    
    // analyse the size of image in provided url and update the maximum sum and result variables
    static public void analyseSizeOfImage(String link) throws Exception
    {
        URL url = new URL(link);
        
        BufferedImage image = ImageIO.read(url);
        int height = image.getHeight(null);
        int width = image.getWidth(null);
        int sum = height + width;
        
        if (sum >= max)
        {
            max = sum;
            result = link;
        }
    }
}
