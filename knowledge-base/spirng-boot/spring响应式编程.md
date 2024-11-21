# 内置FunctionInterface

![[Pasted image 20240204100816.png|625]]
# Stream

创建，中间操作，终止操作

![[Pasted image 20240204102138.png|550]]

>[!note]+ Collectors 是一个终止操作

Collectors.toList()
```java
private final List<String> inheritedClassNames = new ArrayList<>();
this.inheritedClassNames.addAll(Arrays.stream(names).collect(Collectors.toList()));  
```
Collectors.groupingBy()
```java
Map<String, List<Book>> bookMap= Stream.of(new Book(4L, "Three Body", "Novel"),  
new Book(1L, "JAva in Action", "Learning"),  
new Book(2L, "Europe His", "Novel"),  
new Book(3L, "Speech Skills", "Learning")  
).collect(Collectors.groupingBy(Book::getCategory));  
bookMap.entrySet().forEach(entry ->  
System.out.println(String.format("Category:%s, Book detail:%s", entry.getKey(),entry.getValue()))  
);
```

# Java9 Reactive Stream
Publisher -> Subscriber

正压 生产者产生数据
背压 消费者处理数据时的速度
>[!note]+  SubmissionPublisher, Subscriber, Subscription, Processor
![[Pasted image 20240217102449.png|575]]
```java
public static void main(String[] args) throws InterruptedException {
        SubmissionPublisher<String> publisher =new SubmissionPublisher<>();

        Flow.Subscriber<String> subscriber = new Flow.Subscriber<String>() {
            private Flow.Subscription subscription;
            @Override
            public void onSubscribe(Flow.Subscription subscription) {
                System.out.println(Thread.currentThread() + " Start subscription: " + subscription);
                this.subscription = subscription;
                subscription.request(1); // request 1/ALL msg
            }
            @Override
            public void onNext(String item) {
                //subscription.request(1);
                System.out.println(Thread.currentThread() + " Received msg: " + item);
                subscription.request(1);
            }
            @Override
            public void onError(Throwable throwable) {
                System.out.println(Thread.currentThread() + " Received error: " + throwable);
            }
            @Override
            public void onComplete() {
                System.out.println(Thread.currentThread() + " completed");
            }
        };
        publisher.subscribe(subscriber);
        for(int i=0;i<10;i++) {
            publisher.submit("p-" + i);
        }
        //publisher.closeExceptionally(new RuntimeException("bad case"));
        publisher.close();
        Thread.sleep(10000);
    }
```

Proessor will be both publisher and subscriber
```java
    public static class SimpleProcessor extends SubmissionPublisher<String> implements Flow.Subscriber<String> {
        private Flow.Subscription subscription;
        @Override
        public void onSubscribe(Flow.Subscription subscription) {
            this.subscription =subscription;
            this.subscription.request(1);
        }

        @Override
        public void onNext(String item) {
            item = item + " !!!";
            this.submit(item);
            this.subscription.request(1);
        }

        @Override
        public void onError(Throwable throwable) {
            System.out.println(Thread.currentThread() + " on error");
        }

        @Override
        public void onComplete() {
            System.out.println(Thread.currentThread() + " complete");
        }
    }
```

```java
        SimpleProcessor processor1 = new SimpleProcessor();
        SimpleProcessor processor2 = new SimpleProcessor();
        SimpleProcessor processor3 = new SimpleProcessor();

        publisher.subscribe(processor1);
        processor1.subscribe(processor2);
        processor2.subscribe(processor3);
        processor3.subscribe(subscriber);
```

# !!!Reactor

import
```json
dependencies {
    implementation platform('io.projectreactor:reactor-bom:2020.0.31')
    implementation 'io.projectreactor:reactor-core'
}
```


## Mono Flux
```java
    public static void flux() throws InterruptedException {
        Flux<Integer> flux = Flux.just(1,2,3,4,5);
        flux.subscribe(System.out::println);

        Mono<Integer> mono = Mono.just(1);
        mono.subscribe(System.out::println);

        Flux.interval(Duration.ofSeconds(1)).subscribe(System.out::println);
        Thread.sleep(10000);
    }
```

触发事件，在订阅后才会触发
![[Pasted image 20240218113159.png|450]]

![[Pasted image 20240218113726.png|500]]


Use BaseSubscriber to consume msg, and also can ovr methods of consumer
```java
        Flux<Integer> flux = Flux.range(1,10).doOnNext(System.out::println).map(i->i*i).doOnCancel(() -> System.out.println(
                "canceled"
        ));
        flux.subscribe(
                new BaseSubscriber<Integer>(){
                    @Override
                    protected void hookOnNext(Integer value) {
                        if(value<=5) {
                            System.out.println("value: " + value);
                            request(1);
                        } else {
                            cancel();
                        }
                    }
                }
        );
```

doOnXXXX: 事件发生时回调一下
onXXXX：事件发生时，处理的流程，这不是回调，而是改变行为，效果更大 

重塑
Flux  buffer(3) 三个一组组成Arraylist 给subscriber
Flux  limitRate(100) 速率控制 第一次抓100的数据， 消费了75个后再捞75个

数据的创建
同步环境用generate， 异步用create
```java
        Flux.generate(()->0, (pos,sink) -> {
            if(pos<100) {
                pos++;
                sink.next("element: " + pos);
            } else {
                sink.complete();
            }
            return pos;
        }).log().limitRate(10).buffer(3).subscribe(System.out::println);
```

```java
        Flux.create(sink -> {
            for (int ix=1;ix<=100;ix++) {
                sink.next("element: " + ix);
            }
            sink.complete();
        }).log().subscribe(System.out::println);
```
26待续