import JSHOP2.*;
import java.util.*;
import java.lang.reflect.*;
import java.text.NumberFormat;

public class run{
	public static void main(String[] args) {
		long time = System.currentTimeMillis();
		Runtime runtime = Runtime.getRuntime();
		NumberFormat format = NumberFormat.getInstance();
		
		ClassLoader classloader = run.class.getClassLoader();
		try {
			Class aClass = classloader.loadClass(args[0]);
			java.lang.reflect.Method method = aClass.getMethod("getPlans");
			// Object o = method.invoke(null);
// 			java.util.List l = ((java.util.List)o);
// 			System.out.println(l.size()+" plans found!");
// 			System.out.println(o);
			LinkedList<Plan> plans = (LinkedList<Plan>) method.invoke(null);
			// System.out.println(plans);
			time = System.currentTimeMillis() - time;
			System.out.println("Time taken planning: "+(time/1000f)+"s");
			long allocatedMemory = runtime.totalMemory();
			System.out.println("Allocated memory: " + format.format(allocatedMemory / 1024) + "kb");
			System.out.println(plans.size()+" plans found!");
			int planIndex = 1;
			for(Plan plan:plans) {
				System.out.println("Plan "+planIndex);
				System.out.println(plan);
				planIndex++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		//problem.getPlans();
		//new JSHOP2GUI();
	} 
}
