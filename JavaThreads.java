import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.util.ArrayList;
import java.net.URL;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.InputStream;
import javax.imageio.ImageReader;
import java.awt.Image;
import javax.swing.ImageIcon;
import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Nasa_Concurrent
{
    public static void main(String[] args) throws Exception
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
        
        raw = raw.replace("JPG", "jpg").replace ("PNG", "png");
        
        // populate array with String urls
        ArrayList<String> arr = new ArrayList<>();
        while (raw.indexOf("http") !=-1)
        {
            int beg = raw.indexOf(":\"http");
            int end = raw.indexOf(".jpg");
            
            if (end > raw.indexOf(".png") && raw.indexOf(".png") != -1)
            {
                end = raw.indexOf(".png");
            }
            
            if(end == -1)
            {
                end = raw.indexOf(".png");
            }
            
            arr.add(raw.substring(beg+2, end+4));   
            raw = raw.substring(end + 4);
        }
        
        int size = arr.size();
        
        ArrayList<ArrayList<String>> megaArr= new ArrayList<>(); 
        
        // populate 8 arrays with 107 urls each
        for (int j = 0; j < 8; j++)
        {
           // System.out.println("Array is good: " + j);
            ArrayList<String> sList = new ArrayList<>();
            sList.addAll(arr.subList(j*107, j*107+107));
            megaArr.add(sList);
        }
        
        // create 8 threads and provide different url array to each of them for processing
        ExecutorService pool = Executors.newFixedThreadPool(8);
        for (int j = 0; j < 8; j++)
        {
            MyThread  t = new MyThread (j, megaArr.get(j));
            pool.submit(t);
        }
        
        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.DAYS);
        
        // display the time and results
        Instant end = Instant.now();
        System.out.println( Arrays.toString(MyThread.results));
        System.out.println("Time elapsed: " + Duration.between(start, end).toMillis());
    }
}

class MyThread extends Thread
{
    static Object lock = new Object();
    static String[] results = new String[8];
    ArrayList<String> list;
    
    int max, threadNumber;
    String result = "";
    
    public MyThread(int counter, ArrayList<String> list)
    {
        this.threadNumber = counter;
        this.list = list;
    } 
    
    public void run()
    {
        for (int j = 0; j < 107; j++)
        {
            // prepare the link for
            list.set(j, list.get(j).replace("http", "https"));
            list.set(j, list.get(j).replace(".jpl", ""));
            String link = list.get(j);
            
            //do the processing 
            try
            {
                URL url = new URL(link);
                BufferedImage image = ImageIO.read(url);
                
                int height = image.getHeight(null);
                int width = image.getWidth(null);
                int sum = height +width;
            
                if (sum >= max)
                {
                    max = sum;
                    record(link);
                }
            }
           catch (Exception e){}
        }
    }
    
    // update the result array, in thread safe manner
    public void record(String resultUpdated)
    {
        synchronized(lock)
        {
            results[threadNumber] = resultUpdated;
        }
    }
}
