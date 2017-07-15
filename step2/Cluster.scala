import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.clustering.KMeans
import scala.io.Source
import org.apache.spark.sql.functions._


val Batdata = sc.textFile("hdfs://localhost:9000/IPL/Cluster/Input/batData.csv")

// comma separator split
val rows = Batdata.map(line => line.split(","))

// define case class
case class CC1(Batsman_name: String, avgScore: Double, avgStrikeRate: Double)

// map parts to case class
val allBatData = rows.map(p => CC1(p(0).toString, p(1).trim.toDouble, p(2).trim.toDouble))

// convert rdd to dataframe
val allBatDF = allBatData.toDF()

// convert back to rdd and cache the data
val BatrowsRDD = allBatDF.rdd.map(r => (r.getString(0), r.getDouble(1), r.getDouble(2)))
BatrowsRDD.cache()

// convert data to RDD which will be passed to KMeans and cache the data. These are the attributes we want to use to assign the instance to a cluster
val Batvectors = allBatDF.rdd.map(r => Vectors.dense( r.getDouble(1),r.getDouble(2)))
Batvectors.cache()

//KMeans model with 10 clusters and 100 iterations
val BatkMeansModel = KMeans.train(Batvectors, 10, 100)

// Get the prediction from the model with the ID so we can link them back to other information
//maps each data roow with its cluster index it belongs to. 

val Batpredictions = BatrowsRDD.map(r => (r._1, BatkMeansModel.predict(Vectors.dense(r._2,r._3))))

// convert the rdd to a dataframe
val BatpredDF = Batpredictions.toDF("Batsman_name", "CLUSTER")
val BatfinalDF = allBatDF.join(BatpredDF,"Batsman_name")
//Print the center of each cluster
BatkMeansModel.save(sc, "hdfs://localhost:9000/IPL/Cluster/BatsmanCluster")
BatfinalDF.coalesce(1).write.format("com.databricks.spark.csv").option("header","true").save("hdfs://localhost:9000/IPL/Cluster/BatsmanClusterData")






val Bowldata = sc.textFile("hdfs://localhost:9000/IPL/Cluster/Input/bowlData.csv")

// comma separator split
val rows = Bowldata.map(line => line.split(","))

// define case class
case class CC1(Bowler_name: String, Balls: Int, Wickets: Int, Economy: Double)

// map parts to case class
val allBowlData = rows.map(p => CC1(p(0).toString, p(1).trim.toInt, p(2).trim.toInt, p(3).trim.toDouble))

// convert rdd to dataframe
val allBowlDF = allBowlData.toDF()

// convert back to rdd and cache the data
val BowlrowsRDD = allBowlDF.rdd.map(r => (r.getString(0), r.getInt(1), r.getInt(2), r.getDouble(3)))
BowlrowsRDD.cache()

// convert data to RDD which will be passed to KMeans and cache the data. These are the attributes we want to use to assign the instance to a cluster
val Bowlvectors = allBowlDF.rdd.map(r => Vectors.dense( r.getInt(1),r.getInt(2),r.getDouble(3)))
Bowlvectors.cache()

//KMeans model with 10 clusters and 100 iterations
val BowlkMeansModel = KMeans.train(Bowlvectors, 10, 100)

// Get the prediction from the model with the ID so we can link them back to other information
//maps each data roow with its cluster index it belongs to. 

val Bowlpredictions = BowlrowsRDD.map(r => (r._1, BowlkMeansModel.predict(Vectors.dense(r._2,r._3,r._4))))

// convert the rdd to a dataframe
val BowlpredDF = Bowlpredictions.toDF("Bowler_name", "CLUSTER")
val BowlfinalDF = allBowlDF.join(BowlpredDF,"Bowler_name")
//Print the center of each cluster
BowlkMeansModel.save(sc, "hdfs://localhost:9000/IPL/Cluster/BowlerCluster")
BowlfinalDF.coalesce(1).write.format("com.databricks.spark.csv").option("header","true").save("hdfs://localhost:9000/IPL/Cluster/BowlerClusterData")

